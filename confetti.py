"""
Confetti.

An example of how an application could leverage AWS KMS and SSM
as an application parameter vault / configuration manager.
"""

import os

import boto3

import utils.kms


class Confetti(object):
    """Base class to be extended by the application."""

    def __init__(self, **kwargs):
        """Initialize and get application parameters."""
        # Protect these with a leading "_" so they don't interfere with
        # potential parameter names.
        # Also you probably don't want people interacting with these.
        self._key = kwargs.get('key', os.getenv('CONFETTI_KEY', 'Development'))
        self._key_id = 'alias/{}'.format(self._key)
        self._path = '/{}/{}'.format(self._key, self.__class__.__name__)
        self._session = kwargs.get('session', boto3.session.Session())
        self._kms = self._session.client('kms')
        self._ssm = self._session.client('ssm')
        self.parameters = dict()

        response = self._ssm.get_parameters_by_path(
            Path=self._path,
            WithDecryption=True
        )

        for parameter in response['Parameters']:
            name = parameter['Name'].replace(self._path + '/', '')

            self.parameters[name] = parameter["Value"]

    def __getattr__(self, attribute):
        """Override __getattr__ to return None on empty parameters."""
        # When we attempt to get an attribute that doesn't exist on the object,
        # instead we're actually trying to get it from self.parameters
        return self.parameters.get(attribute)

    def __getitem__(self, key):
        """Perform getitem on parameters retrieved from the store."""
        # If we're holding on to the parameters as a dictionary it makes
        # key-retrieval easy!
        return self.parameters[key]

    def __iter__(self):
        """Iterate over parameters retrieved from kms."""
        # If we have a dictionary as the storage for the parameters we can
        # let people iterate on the storage keys too!
        return dict(self.parameters)

    def __repr__(self):
        """Override __repr__ with a representation of self."""
        return "{}(path='{}', session={})".format(
            self.__class__.__name__,
            self._path,
            self._session
        )

    def __str__(self):
        """Get the string value of self."""
        return repr(self)

    def put_parameters(self, parameters):
        """Put parameters to AWS Systems Manager parameter store."""
        for parameter in parameters:
            if not parameter['Name'].startswith(self._path):
                parameter['Name'] = '/'.join([self._path, parameter['Name']])

            if parameter['Type'] == 'SecureString':
                parameter['KeyId'] = self._key_id

            utils.kms.ensure_key(self._kms, self._key_id, self._key)
            self._ssm.put_parameter(**parameter)
