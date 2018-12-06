"""AWS Key Management Service ancillary functions."""

import botocore


def key_exists(client, key_id):
    """Check that the encryption key exists."""
    try:
        client.describe_key(KeyId=key_id)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'NotFoundException':
            return False
        else:
            raise e

    return True


def ensure_key(client, alias_name, **kwargs):
    """
    Create the encryption key if it doesn't exist.

    New keys will be aliased and have key rotation enabled.
    """
    if not key_exists(client, alias_name):
        response = client.create_key(**kwargs)
        key_id = response["KeyMetadata"]["KeyId"]

        client.enable_key_rotation(KeyId=key_id)
        client.create_alias(AliasName=alias_name, TargetKeyId=key_id)
