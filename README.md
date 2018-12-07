Confetti
=========
Confectionary confetti to confine those confounded configurations confidently
---------

## Install in your application
```bash
$ pip install git+ssh://git@github.com/AmberEngine/confectionary-confetti.git#egg=confectionary-confetti
```

## A boto3 session will be created from your AWS config and credentials or role or you can override the session.
```python
    session = boto3.session.Session()
    config = Confetti(session=session)
```

## Choose a key. Your key will be part of the namespacing of your application's parameters and will be used as an alias for a KMS key to encrypt and decrypt your parameters.
```bash
$ export CONFETTI_KEY=YourKey
```

### Optionally you can override this in the constructor's keyword arguments.
```python
    config = Confetti(confetti_key='YourKey')
```
The default value is 'Development' if neither is specified.

## Choose a path for the namespacing of your application's parameters.
```bash
$ export CONFETTI_PATH=Your/Path
```

### Optionally you can override this in the constructor's keyword arguments.
```python
    config = Confetti(confetti_path='Your/Path')
```
The default value will be the class name if neither is specified.

The parameter store path will be constructed as `/<confetti_key>/<confetti_path>`

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

## Store parameters from a JSON file.

### Create a JSON file with your new parameters
```json
[{
    "Name": "APP_URL",
    "Value": "http://www.mrcoolice.com/app",
    "Type": "String"
}, {
    "Name": "APP_KEY",
    "Value": "abcde12345",
    "Type": "SecureString"
}, {
    "Name": "THINGS",
    "Value": "thing1, thing2",
    "Type": "StringList"
}]
```

## Export your current parameters to a JSON file so you can modify them.
```python
    from confetti import Confetti

    # Create your app's config
    confetti = Confetti(confetti_key="Production", confetti_path="MyApp")
    config = confetti.get()

    # Export to JSON
    config.export_parameters("example.json")
```

### Review and modify your parameters.
```json
[{
    "Name": "APP_URL",
    "Value": "http://www.mrcoolice.com/app",
    "Type": "String",
    "Overwrite": true
}, {
    "Name": "APP_KEY",
    "Value": "abcde12345",
    "Type": "SecureString",
    "Overwrite": true
}, {
    "Name": "THINGS",
    "Value": "thing1, thing2",
    "Type": "StringList",
    "Overwrite": true
}]
```

## Set your parameters for your application.  Do this only once and your parameters will be stored in your AWS SSM Parameter Store.
```python
    from confetti import Confetti

    # Create your app's config
    confetti = Confetti(confetti_key="Production", confetti_path="MyApp")

    # Set parameters in the parameter store
    config.set("example.json")
```

see also: [AWS Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-paramstore.html) [SSM.Client.put_parameter](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.put_parameter)
