"""Confetti."""

import json
import logging
import os

import boto3
import botocore

import utils.kms


class Confetti(object):
    """Base class Confetti can be extended by the application."""

    def __init__(self, confetti_key=None, confetti_app=None, session=None):
        """Initialize and get application parameters."""
        # Passing confetti_key as an argument to the constructor
        # overrides the environment variable CONFETTI_KEY.
        # The default value is 'Development' in either case.
        self.confetti_key = confetti_key \
            if confetti_key \
            else os.getenv('CONFETTI_KEY', 'Development')

        # Passing confetti_app as an argument to the constructor
        # overrides the environment variable CONFETTI_KEY.
        # The default value is the class name in either case.
        self.confetti_app = confetti_app \
            if confetti_app \
            else os.getenv('CONFETTI_APP', self.__class__.__name__)

        # Override the default session by supplying a custom session
        # to the constructor.
        self.session = session if session else boto3.session.Session()

        # Protect these with a leading "_" so they don't interfere with
        # potential parameter names.
        # Also you probably don't want people interacting with these.
        self._path = '/{}/{}'.format(self.confetti_key, self.confetti_app)
        self._kms = self.session.client('kms')
        self._ssm = self.session.client('ssm')

        self.get_parameters()

    def __getattr__(self, attribute):
        """
        Override getattr.

        When we attempt to get an attribute that doesn't exist on the object,
        instead we're actually trying to get it from self.parameters
        """
        return self.parameters.get(attribute, None)

    def __getitem__(self, key):
        """
        Override getitem.

        Parameters are retrieved from the dictionary.
        """
        return self.parameters[key]

    def __iter__(self):
        """
        Override iter.

        Parameters are iterable.
        """
        return dict(self.parameters)

    def __repr__(self):
        """
        Override repr.

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
        """Get parameters from AWS Systems Manager parameter store."""
        self.parameters = dict()

        for parameter in self._ssm.get_parameters_by_path(
            Path=self._path,
            WithDecryption=True
        ).get('Parameters'):
            name = parameter['Name'].replace(self._path + '/', '')

            self.parameters[name] = parameter["Value"]

    def put_parameters(self, parameters):
        """Put parameters to AWS Systems Manager parameter store."""
        key_id = 'alias/{}'.format(self.confetti_key)
        description = self.confetti_key
        message = '{}: {}: {}'
        logger = self.get_logger()

        utils.kms.ensure_key(self._kms, key_id, description)

        for parameter in parameters:
            if not parameter['Name'].startswith(self._path):
                parameter['Name'] = '/'.join([self._path, parameter['Name']])

            if parameter['Type'] == 'SecureString':
                parameter['KeyId'] = key_id

            try:
                self._ssm.put_parameter(**parameter)
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code']:
                    logger.warning(
                        message.format(
                            e.response['Error']['Code'],
                            parameter['Name'],
                            e.response['Error']['Message']
                        )
                    )
                else:
                    raise e

    def import_parameters(self, json_file):
        """Import parameters from a json file."""
        parameters = []

        with open(json_file) as in_file:
            parameters = json.load(in_file)

        if parameters:
            self.put_parameters(parameters)
