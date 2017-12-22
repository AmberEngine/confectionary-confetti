"""Confetti.

Confectionary confetti to confine those confounded configurations confidently.
"""

import json
import logging
import os

import boto3
import botocore

import utils.kms


class Confetti(object):
    """Base class Confetti can be extended by the application."""

    def __init__(self, confetti_key=None, confetti_app=None, session=None):
        """Initialize and get application parameters.

        Set the AWS SSM parameter store path to /<confetti_key>/<confetti_app>
        and get parameters by path.

        :param confetti_key: the encryption key name
                             overrides CONFETTI_KEY environment variable
                             defaults to Development
        :param confetti_app: the application name
                             overrides CONFETTI_APP environment variable
                             defaults to the class name
        :param session: a boto3 session
                        defaults to the default session
        """
        self.confetti_key = confetti_key \
            if confetti_key \
            else os.getenv('CONFETTI_KEY', 'Development')
        self.confetti_app = confetti_app \
            if confetti_app \
            else os.getenv('CONFETTI_APP', self.__class__.__name__)
        self.confetti_path = '/{}/{}'.format(
            self.confetti_key,
            self.confetti_app
        )
        self.session = session \
            if session \
            else boto3.session.Session()

        self.get_parameters()

    def __getattr__(self, attribute):
        """Override getattr.

        When we attempt to get an attribute that doesn't exist on the object,
        instead we're actually trying to get it from self.parameters

        :param attribute: the config atribute
        :type attribute: str
        """
        return self.parameters.get(attribute, None)

    def __getitem__(self, key):
        """Override getitem.

        Parameters are retrieved from the dictionary.

        :param key: the config attribute name
        :type key: str
        """
        return self.parameters[key]

    def __iter__(self):
        """Override iter.

        Parameters are iterable.
        """
        return dict(self.parameters)

    def __repr__(self):
        """Override repr.

        Create a string representation that is unambiguous so that
        eval(repr(Confetti(**parameters))) == Confetti(**parameters)
        """
        return "{}(confetti_key='{}', confetti_app='{}', session={})".format(
            self.confetti_key,
            self.confetti_app,
            self.session
        )

    def __str__(self):
        """Get the string value of self."""
        return repr(self)

    def get_logger(self):
        """Get a logger."""
        return logging.getLogger(self.confetti_app)

    def get_parameters(self):
        """Get parameters from AWS SSM parameter store by path."""
        self.parameters = dict()
        ssm = self.session.client('ssm')

        for parameter in ssm.get_parameters_by_path(
            Path=self.confetti_path,
            WithDecryption=True
        ).get('Parameters'):
            name = parameter['Name'].replace(self.confetti_path + '/', '')

            self.parameters[name] = parameter["Value"]

    def put_parameters(self, parameters):
        """Put parameters to AWS Systems Manager parameter store.

        Ensures the following:
          - the encryption key exists
          - parameter names are prefixed with the path
          - secure parameters use the correct key

        :param parameters: the list of parameters
        :type parameters: list
        """
        key_id = 'alias/{}'.format(self.confetti_key)
        description = self.confetti_key
        message = '{}: {}: {}'
        logger = self.get_logger()
        kms = self.session.client('kms')
        ssm = self.session.client('ssm')

        utils.kms.ensure_key(kms, key_id, description)

        for parameter in parameters:
            if not parameter['Name'].startswith(self.confetti_path):
                parameter['Name'] = '/'.join([
                    self.confetti_path, parameter['Name']
                ])

            if parameter['Type'] == 'SecureString':
                parameter['KeyId'] = key_id

            try:
                ssm.put_parameter(**parameter)
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == 'ParameterAlreadyExists':
                    logger.warning(
                        message.format(
                            e.response['Error']['Code'],
                            parameter['Name'],
                            e.response['Error']['Message']
                        )
                    )
                else:
                    raise e

    def import_parameters(self, file_name):
        """Import parameters from a JSON file.

        The parameters are a list of parameters to the
        boto3 SSM client method put_parameter.

        :param file_name: the file name containing the JSON parameters
        :type file_name: str

        :Example:

        [{
            "Name": "APP_URL",
            "Description": "The URL",
            "Value": "http://www.mrcoolice.com/app",
            "Type": "String"
        }, {
            "Name": "APP_KEY",
            "Description": "All my passwords and PINs in one parameter",
            "Value": "abcde12345",
            "Type": "SecureString"
        }]
        """
        parameters = []

        with open(file_name) as in_file:
            parameters = json.load(in_file)

        if parameters:
            self.put_parameters(parameters)
