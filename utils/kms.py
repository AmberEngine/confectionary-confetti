"""AWS Key Management Service ancillary functions."""

import botocore


def key_exists(kms, key_id):
    """
    Check that the encryption key exists and it's enabled.

    If the key exists, but isn't enabled, the caller needs to figure out why.
    :param
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


def ensure_key(kms, key_id, description):
    """
    Create the encryption key.

    If it doesn't exist and create an alias.
    """
    if not key_exists(kms, key_id):
        response = kms.create_key(Description=description)
        key_metadata = response['KeyMetadata']

        kms.create_alias(AliasName=key_id, TargetKeyId=key_metadata['KeyId'])
        kms.enable_key_rotation(KeyId=key_metadata['KeyId'])
