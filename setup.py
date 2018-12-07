"""Confetti configuration utility."""
import os
from setuptools import setup, find_packages


def get_description(file_name='README.md'):
    """Get contents of a file as a string or empty string if none exists."""
    path = os.path.join(os.path.dirname(__file__), file_name)

    if os.path.exists(path):
        with open(path) as in_file:
            return in_file.read()

    return __doc__


arguments = {
    'name': 'confectionary-confetti',
    'version': '0.1',
    'description': __doc__,
    'long_description': get_description(),
    'license': 'Other/Proprietary License',
    'packages': find_packages(),
}

setup(**arguments)
