Confetti
=========

## Install in your application

```bash
$ pip install -e git+git@github.com:AmberEngine/confetti.git#egg=confetti
```

## Choose a key. Your key will be your application's namespace
```bash
$ export CONFETTI_KEY=YourKey
```

## Extend in your application
```python
"""Example application."""

from confetti import Confetti


class MrCoolIceApp(Confetti):
    """
    Test example implementation.

    You can add extra vars here if you need to.
    """

    pass
```

## Store some parameters (this will probably become a cli of some sort)
```python
    config = MrCoolIceApp()
    parameters = [{
        'Name': 'APP_URL',
        'Description': 'The URL',
        'Value': 'http://www.mrcoolice.com/app',
        'Type': 'String'
    }, {
        'Name': 'APP_KEY',
        'Description': 'All my passwords and PINs in one parameter',
        'Value': 'abcde12345',
        'Type': 'SecureString'
    }]

    config.put_parameters(parameters)
```

## Use your parameters in your application
```python
    config = MrCoolIceApp()

    print(config.APP_URL)
```

## Your Friendly Neighborhood Repository Owner

[![Jim Garner](https://avatars2.githubusercontent.com/u/9437566?v=3&s=100)](https://github.com/jg75)

[Jim Garner](https://github.com/jg75)
