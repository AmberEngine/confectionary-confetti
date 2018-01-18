"""AWS Systems Management Service ancillary functions."""

def get_parameters_by_path(ssm, **kwargs):
    """Get parameters from AWS SSM parameter store by path."""

    parameters = []

    while True:
        response = ssm.get_parameters_by_path(**kwargs)
        kwargs['NextToken'] = response.get('NextToken')
        parameters += response.get('Parameters')

        if not kwargs.get('NextToken'):
            break

    return parameters
