"""AWS Key Management Service ancillary functions."""

import botocore


def key_exists(kms, key_id):
    """Check that the encryption key exists.

    :param key_id: the encryption key id, alias or arn
    :type key_id: str
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


def ensure_key(kms, alias_name, description):
    """Create the encryption key if it doesn't exist.

    New keys will be aliased and have key rotation enabled.

    :param alias_name: the encryption key alias
    :param description: a description of the key
    :type alias_name: str
    :type description: str
    """

    if not key_exists(kms, alias_name):
        response = kms.create_key(Description=description)
        key_metadata = response['KeyMetadata']

        kms.enable_key_rotation(KeyId=key_metadata['KeyId'])
        kms.create_alias(
            AliasName=alias_name,
            TargetKeyId=key_metadata['KeyId']
        )
