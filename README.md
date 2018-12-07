Confetti
=========
Confectionary confetti to confine those confounded configurations confidently
---------

### Install in your application
```bash
$ pip install boto3
$ pip install git+ssh://git@github.com/AmberEngine/confectionary-confetti.git#egg=confectionary-confetti
```

**You need to install `boto3` if it is not already installed.**
`boto3` is **not** a listed package dependency of `confetti`.

On AWS Lambda functions `boto3` is already present. To include it would result
in exceeding the allowed size for lambda code.

It is easier to instead have projects install _both_ `confetti` and `boto3` manually.

## Choose a key. Your key will be part of the namespacing of your application's parameters and will be used as an alias for a KMS key to encrypt and decrypt your parameters.
```bash
$ export CONFETTI_KEY=YourKey
```
Optionally you can override this in the constructor's keyword arguments.
```python
    config = Confetti(confetti_key='YourKey')
```
The default value is 'Development' if neither is specified.

## Choose a path for the namespacing of your application's parameters.
```bash
$ export CONFETTI_PATH=Your/Path
```
Optionally you can override this in the constructor's keyword arguments.
```python
    config = Confetti(confetti_path='Your/Path')
```
The path will be constructed as ```/<confetti_key>/<confetti_path>```

The default value will be the class name if neither is specified.

## A boto3 session will be created from your AWS config and credentials or role or you can override the session.
```python
    session = boto3.session.Session()
    config = Confetti(session=session)
```

## Retrieve and use your parameters in your application.
```python
    from confetti import Confetti

    confetti = Confetti(confetti_key="Production", confetti_path="MyApp")
    config = confetti.get()

    # Print a specific parameter
    print(config.APP_URL)

    # Print your parameters
    print(config)
```

## As an alternative to using the AWS Systems Manager console, you can store parameters by importing from a JSON file.
see also: [AWS Systems Manager Parameter Store](https://console.aws.amazon.com/systems-manager/parameters)
see also: [Boto3 SSM.Client.put_parameter](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.put_parameter)

### Create a JSON file with your new parameters
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

### Or export your current parameters to a JSON file so you can modify them.
```python
    from confetti import Confetti

    # Create your app's config
    confetti = Confetti(confetti_key="Production", confetti_path="MyApp")
    config = confetti.get()

    # Export to JSON
    config.export_parameters("example.json")
```
```json
[{
    "Name": "APP_URL",
    "Description": "The URL",
    "Value": "http://www.mrcoolice.com/app",
    "Type": "String",
    "Overwrite": True
}, {
    "Name": "APP_KEY",
    "Description": "All my passwords and PINs in one parameter",
    "Value": "abcde12345",
    "Type": "SecureString",
    "Overwrite": True
}, {
    "Name": "THINGS",
    "Description": "All the things",
    "Value": "thing1, thing2",
    "Type": "StringList",
    "Overwrite": True
}]
```

### Set your parameters for your application.  Do this only once and your parameters will be stored in your AWS SSM Parameter Store.
```python
    from confetti import Confetti

    # Create your app's config
    confetti = Confetti(confetti_key="Production", confetti_path="MyApp")

    # Set parameters in the parameter store
    config.set("example.json")
```
