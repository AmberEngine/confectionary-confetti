Confetti
=========
Confectionary confetti to confine those confounded configurations confidently
---------

### Install in your application
In order to complete the install for `confetti` you need to install the
`boto3` library. It is required for `contetti` to run.

`boto3` is **not** an python package dependency of `confetti` because it is 
available on AWS Lambda functions and to include it would end up exceeding
the allowed size for lambda code. It is easier to instead have projects install
_both_ `confetti` and `boto3` manually.

Run the following to get the latest versions of both:
```bash
$ pip install boto3
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

## As an alternative to using the AWS Systems Manager console, you can store parameters by importing from a JSON file.
see also: [AWS Systems Manager Parameter Store](https://console.aws.amazon.com/systems-manager/parameters)
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
