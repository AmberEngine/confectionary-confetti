"""Confetti."""
import os
from setuptools import setup, find_packages


def get_description(file_name='README.md'):
    """Get contents of a file as a string or empty string if none exists.

    :param file_name: The name of the file containing the description
    """
    path = os.path.join(os.path.dirname(__file__), file_name)
    description = ""

    if os.path.exists(path):
        with open(path) as in_file:
            long_description = in_file.read()

    return description


arguments = {
    'name': 'confectionary-confetti',
    'version': '0.1',
    'description': __doc__,
    'long_description': get_description(),
    'license': 'Other/Proprietary License',
    'packages': find_packages(),
}

setup(**arguments)
