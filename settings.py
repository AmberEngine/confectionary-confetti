"""
An example of how an application could leverage AWS KMS and SSM
as an application parameter vault / configuration manager.
"""

import os

import boto3


class Settings:
    path = '/{}/{}'.format(
        os.getenv('APP_ENV', 'development'),
        'mrcooliceapp'
    )

    def __init__(self, session):
        self.session = session
        self.kms = session.client('kms')
        self.ssm = session.client('ssm')

        self.get_parameters()


    def get_parameters(self):
        response = self.ssm.get_parameters_by_path(
            Path=self.path,
            WithDecryption=True
        )

        for parameter in response['Parameters']:
            name = parameter['Name'].replace(self.path + '/', '')

            setattr(self, name, parameter['Value'])


# Test usage
if __name__ == '__main__':
    settings = Settings(boto3.session.Session(region_name='us-east-1'))

    print(settings.APP_URL)
