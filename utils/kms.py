"""Some AWS KMS library shit that I can use again later."""

import boto3
import botocore


def key_exists(kms, key_id):
    """
    Check that the encryption key exists and it's enabled.
    If the key exists, but isn't enabled,
    the caller needs to figure out why.
    """
    try:
        kms.describe_key(KeyId=key_id)

        return True
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'NotFoundException':
            pass
        else:
            raise e

    return False


def ensure_key(kms, key_id):
    """
    Create the encryption key if it doesn't exist and create an alias.
    """
    if not key_exists(kms, key_id):
        response = kms.create_key(Description=environment)
        key_metadata = response['KeyMetadata']

        kms.create_alias(AliasName=key_id, TargetKeyId=key_metadata['KeyId'])
        kms.enable_key_rotation(KeyId=key_metadata['KeyId'])


# Test usage
if __name__ == '__main__':
    session = boto3.session.Session(region_name='us-east-1')
    environment = 'development'
    application = 'mrcooliceapp'
    key_id = 'alias/{}'.format(environment)
    path = '/{}/{}'.format(environment, application)
    kms = session.client('kms')
    ssm = session.client('ssm')
    parameters = [{
        'Name': '{}/{}'.format(path, 'APP_URL'),
        'Description': 'This parameter sets the thing'
        'that plugs the thing into the thing',
        'Value': 'http://www.mrcoolice.com/app',
        'Type': 'String',
        'Overwrite': True
    }, {
        'Name': '{}/{}'.format(path, 'APP_KEY'),
        'Description': 'All my passwords and PINs in one parameter',
        'Value': 'abcde12345',
        'Type': 'SecureString',
        'KeyId': key_id,
        'Overwrite': True
    }]

    ensure_key(kms, key_id)

    for parameter in parameters:
        print(parameter)
        ssm.put_parameter(**parameter)
