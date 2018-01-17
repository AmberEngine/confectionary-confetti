Confetti
=========
Confectionary confetti to confine those confounded configurations confidently
---------

### Install in your application
```bash
$ pip install git+ssh://git@github.com/AmberEngine/confectionary-confetti.git#egg=confectionary-confetti
```

## Choose a key. Your key will be part of the namespacing of your application's parameters.
```bash
$ export CONFETTI_KEY=YourKey
```
Optionally you can override this in the constructor's keyword arguments.
```python
    config = Confetti(confetti_key='YourKey')
```
The default value will be 'Development' in either case.

## Choose an app name. Your app name will be part of the namespacing of your application's parameters.
```bash
$ export CONFETTI_APP=YourApp
```
Optionally you can override this in the constructor's keyword arguments.
```python
    config = Confetti(confetti_app='YourApp')
```
The default value will be the class name in either case.

## A boto3 session will be created from your AWS config and credentials or role or you can override the session.
```python
    session = boto3.session.Session()
    config = Confetti(session=session)
```

## Example: extend Confetti in your application
```python
"""Example Docker serivce provisioner.

This Morpheus docker service provisioner runs as a service when the 
Morpheus service starts, and performs some basic provisioning operations
before exiting, including, but not limited to:
pushing updated parameter values to the parameter store via import,
create/update database user(s)/role(s),
run database migrations,
reload/refresh databse data,
run datafixes
"""

import os

from aws.utils.pg_utils import PostgresCursor
from confetti import Confetti


class Provisioner(Confetti):
    """Provisioner."""

    def get_provisioner_data(self):
        """Get the location of the provisioner data."""

        return os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'data',
            self.confetti_key.lower(),
            self.confetti_app.lower()
        )

    def get_statements(self, file_name):
        """Get SQL statements."""
        statements = []

        if os.path.exists(file_name):
            with open(file_name) as in_file:
                for line in in_file:
                    statements.append(line.strip().format(**self.parameters))

        return statements

    def provision_postgres(self, file_name):
        """Provision postgres database."""

        connection = {
            'user': self.ADMIN_DB_USER,
            'password': self.ADMIN_DB_PASSWORD,
            'host': self.ADMIN_DB_HOST,
            'port': self.ADMIN_DB_PORT,
            'dbname': self.ADMIN_DB_NAME
        }

        with PostgresCursor(**connection) as cursor:
            for statement in self.get_statements(file_name):
                try:
                    cursor.execute(statement)
                except Exception as e:
                    print('{} [{}]'.format(e.pgerror.strip(), statement))


class Morpheus(Provisioner):
    """Morpheus provisioner."""

    def provision(self):
        """Provision morpheus and add parameters to the parameter store.

        data/<confetti_key>/<confetti_app>.json  parameters
        data/<confetti_key>/<confetti_app>.sql   sql statements
        """
        data_file = self.get_provisioner_data()

        self.import_parameters('{}.json'.format(data_file))
        self.get_parameters()
        self.provision_postgres('{}.sql'.format(data_file))


if __name__ == '__main__':
    Morpheus().provision()
```

## Store parameters by importing from a JSON file.
```json
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
}, {
    "Name": "THINGS",
    "Description": "All the things",
    "Value": "thing1, thing2",
    "Type": "StringList"
}]
```

```python
    # Create YourApp's config
    config = YourApp()

    # Import from JSON
    config.import_parameters('example.json')
```

## Or export parameters to a JSON file so you can modify in bulk.
```python
    # Create YourApp's config
    config = YourApp()

    # Export to JSON
    config.export_parameters('example.json')
```

### Use your parameters in your application
```python
    config = YourApp()

    # Print a specific parameter
    print(config.APP_URL)

    # Print a dictionary of your parameters
    print(config.parameters)
```

### Your Friendly Neighborhood Repository Owner

[![Jim Garner](https://avatars2.githubusercontent.com/u/9437566?v=3&s=100)](https://github.com/jg75)

[Jim Garner](https:/github.com/jg75)
