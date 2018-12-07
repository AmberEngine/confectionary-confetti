Confetti
=========
Confectionary confetti to confine those confounded configurations confidently
---------

## Install in your application
```bash
$ pip install git+ssh://git@github.com/AmberEngine/confectionary-confetti.git#egg=confectionary-confetti
```

## Create a boto3 session. If you don't create a session, one will be created for you using your AWS user configuration or role.

### The session keyword argument overrides the default session.
```python
    from confetti import Confetti
    
    session = boto3.session.Session()
    confetti = Confetti(session=session)
    
    print(confetti.path)
```
### Output
```
/Development/Confetti
```

## Choose a key. Your key will the root of the namespacing path of your application's parameters and will be used as an alias for a KMS key to encrypt and decrypt your parameters. If you don't choose a key, the default value is 'Development'.

### Set CONFETTI_KEY environment variable. The CONFETTI_KEY environment overrides the default.
```bash
$ export CONFETTI_KEY=YourKey
```
```python
    from confetti import Confetti
    
    confetti = Confetti()
    
    print(confetti.path)
```
### Output
```
/YourKey/Confetti
```

### The confetti_key keyword argument overrides the CONFETTI_KEY environment variable.
```python
    from confetti import Confetti
    
    confetti = Confetti(confetti_key='YourKey')
    
    print(confetti.path)
```
### Output
```
/YourKey/Confetti
```

## Choose a path.  Your path will be appended to the namespacing path of your application's parameters, i.e. /<confetti_key>/<confetti_path>. e.g. /YourKey/Your/Path. If you don't choose a path, the default value is the name of the Confetti class.

### Override the Confetti class and use MyApp as the default.
```python
    from confetti import Confetti
    
    class MyApp(Confetti):
        pass
    
    confetti = MyApp()
    
    print(confetti.path)
```
### Output
```
/Development/MyApp
```

### Set CONFETTI_PATH environment variable. The CONFETTI_PATH environment overrides the default.
```bash
$ export CONFETTI_PATH=Your/Path
```
```python
    from confetti import Confetti
    
    confetti = Confetti()
    
    print(confetti.path)
```
### Output
```
/Development/Your/Path
```

### The confetti_path keyword argument overrides the CONFETTI_PATH environment variable.
```python
    from confetti import Confetti
    
    confetti = Confetti(confetti_path='Your/Path')
    
    print(confetti.path)
```
### Output
```
/Development/Your/Path
```

## Retrieve and use your parameters in your application. Note that it is assumed that your SecureString parameters are to be retrieved with decryption. You can override the parameters to SSM.Client.get_parameters_by_path via keyword arguments with the exception of 'Path'.
```python
    from confetti import Confetti

    confetti = Confetti(confetti_key="Production", confetti_path="MyApp")
    parameters = confetti.get_parameters()

    # Print the value of a specific parameter
    print(parameters.APP_URL)

    # Print your parameters
    print(parameters)
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

## Export your current parameters to a JSON file so you can modify them.  Note that it is assumed that your SecureString parameters are to be retrieved with decryption. You can override the parameters to SSM.Client.get_parameters_by_path via keyword arguments with the exception of 'Path'.
```python
    from confetti import Confetti

    # Create your app's config
    confetti = Confetti(confetti_key="Production", confetti_path="MyApp")

    # Export to JSON from AWS SSM parameter store
    confetti.export_parameters("parameters.json")
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

    # Import parameters from JSON to AWS SSM parameter store
    confetti.import_parameters("parameters.json")
```

see also: [AWS Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-paramstore.html) and [SSM.Client.put_parameter](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.put_parameter)
