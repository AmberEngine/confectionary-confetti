"""Confetti."""
import os
from setuptools import setup, find_packages


def get_app_directory():
    """Get the location of this application."""

    directory = os.path.dirname(__file__)

    if not directory:
        directory = os.getcwd()

    return directory


def get_dependency_links(file_name='dependency_links.txt'):
    """Get the dependency links as a list."""

    path = os.path.join(get_app_directory(), file_name)
    dependency_links = []

    if os.path.exists(path):
        with open(os.path.join(path)) as in_file:
            dependency_links = [line.strip() for line in in_file]

    return dependency_links


def get_description(file_name='README.md'):
    """Get contents of a file as a string or empty string if none exists."""

    path = os.path.join(get_app_directory(), file_name)

    if os.path.exists(path):
        with open(path) as in_file:
            return in_file.read()

    return None


arguments = {
    'name': 'confectionary-confetti',
    'version': '0.1',
    'description': __doc__,
    'long_description': get_description(),
    'license': 'Other/Proprietary License',
    'install_requires': [
        'boto3>=1.5',
    ],
    'dependency_links': get_dependency_links(),
    'packages': find_packages(),
}

setup(**arguments)
