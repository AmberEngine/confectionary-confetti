"""Confetti.

Confectionary confetti to confine those confounded configurations confidently.
"""

import json
import logging
import os

import boto3
import botocore

import confetti.utils.kms as kms_utils
import confetti.utils.ssm as ssm_utils


class Confetti(object):
    """Base class Confetti can be extended by the application."""

    def __init__(
        self,
        confetti_path=None,
        confetti_key=None,
        confetti_app=None,
        session=None,
        recursive=False,
    ):
        """Initialize and get application parameters.

        If confetti_path is no provided, then set the AWS SSM parameter store
        path to /<confetti_key>/<confetti_app> and get parameters by path.

        :param confetti_path: the SSM parameter store path
        :param confetti_key: the encryption key name
                             overrides CONFETTI_KEY environment variable
                             defaults to Development
        :param confetti_app: the application name
                             overrides CONFETTI_APP environment variable
                             defaults to the class name
        :param session: a boto3 session
                        defaults to the default session
        :param recursive: whether to recursively read parameters under the
                          confetti_path. Defaults to False.
        """
        if not confetti_key:
            confetti_key = os.getenv('CONFETTI_KEY', 'Development')

        if not confetti_app:
            confetti_app = os.getenv('CONFETTI_APP', self.__class__.__name__)

        if not confetti_path:
            if not confetti_key or not confetti_app:
                raise ValueError("must specify confetti path, or key and app.")
            confetti_path = f'/{confetti_key}/{confetti_app}'

        if not session:
            session = boto3.session.Session()

        self.confetti_key = confetti_key
        self.confetti_app = confetti_app
        self.confetti_path = confetti_path
        self.session = session
        self.recursive = recursive

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
        return self.parameters[key].value

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
        template = "{}(confetti_key='{}', confetti_app='{}', " \
                   "confetti_path='{}', session={}, recursive={})"
        return template.format(
            self.__class__.__name__,
            self.confetti_key,
            self.confetti_app,
            self.confetti_path,
            self.session,
            self.recursive,
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
        parameters = ssm_utils.get_parameters_by_path(
            ssm,
            Path=self.confetti_path,
            Recursive=self.recursive,
        )

        for parameter in parameters:
            name = parameter['Name'].replace(self.confetti_path + '/', '')
            value = parameter['Value']
            attributes = dict()

            if parameter['Type'] == 'SecureString':
                attributes['encrypted'] = value
                attributes['decrypted'] = ssm.get_parameter(
                    Name=parameter['Name'],
                    WithDecryption=True
                ).get('Parameter').get('Value')
                value = attributes['decrypted']

            self.parameters[name] = self.Parameter(value, **attributes)

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

        kms_utils.ensure_key(kms, key_id, description)

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

    def export_parameters(self, file_name):
        """Write parameters to a JSON file.

        The parameters are a list of parameters to the
        boto3 SSM client method put_parameter.

        :param file_name: the file name containing the JSON parameters
        :type file_name: str
        """
        ssm = self.session.client('ssm')
        parameters = ssm_utils.get_parameters_by_path(
            ssm,
            Path=self.confetti_path
        )

        if parameters:
            with open(file_name, 'w') as out_file:
                out_file.write(json.dumps(parameters))

    class Parameter(object):
        """The object used by confetti to hold config attribute values."""

        def __init__(self, value, **attributes):
            """Initialize a new Parameter."""
            self.value = value
            self.decrypted = attributes.get('decrypted')
            self.encrypted = attributes.get('encrypted')

        def __repr__(self):
            """Override repr."""
            return "\'{}\'".format(self.value)

        def __str__(self):
            """Override str."""
            return self.value
