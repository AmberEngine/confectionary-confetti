Confetti
=========
Confectionary confetti to confine those confounded configurations confidently
---------

### Install in your application

```bash
$ pip install -e git+git@github.com:AmberEngine/confetti.git#egg=confetti
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

## Or you could just extend Confetti in your application
```python
"""Example application."""

from confetti import Confetti


class YourApp(Confetti):
    """
    Test example implementation.

    You can add extra vars here if you need to.
    """

    pass

config = YourApp()
```

## Store some parameters by importing from a JSON file.
see: http://boto3.readthedocs.io/en/latest/reference/services/ssm.html#SSM.Client.put_parameter
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

    # Reload from AWS SSM
    config.get_parameters()
```

### Use your parameters in your application
```python
    config = YourApp()

    print(config.APP_URL)
```

### Your Friendly Neighborhood Repository Owner

[![Jim Garner](https://avatars2.githubusercontent.com/u/9437566?v=3&s=100)](https://github.com/jg75)

[Jim Garner](https:/github.com/jg75)
