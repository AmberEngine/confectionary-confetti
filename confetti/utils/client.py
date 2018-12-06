"""Boto3 Client utility."""


class ClientResponseGenerator:
    """Boto3 Client response generator."""

    def __init__(self, client):
        """Override init method."""
        self.client = client

    def generate_paginated(self, operation, key, **kwargs):
        """Generate a paginated client response."""
        paginator = self.client.get_paginator(operation)
        response_iterator = paginator.paginate(**kwargs)

        for response in response_iterator:
            for result in response[key]:
                yield result

    def generate_unpaginated(self, operation, key, **kwargs):
        """Generate an unpaginated client response."""
        response = getattr(self.client, operation)(**kwargs)

        for result in response[key]:
            yield result

    def get(self, operation, key, **kwargs):
        """Get the response generator."""
        if self.client.can_paginate(operation):
            return self.generate_paginated(operation, key, **kwargs)
        else:
            return self.generate_unpaginated(operation, key, **kwargs)
