"""Confetti."""
import os
import sys

from pip import req
from setuptools import setup, find_packages


def get_app_directory():
    """Get the location of this application."""

    directory = os.path.dirname(__file__) 

    if not directory:
        directory = os.getcwd()

    return directory


def get_requirements(file_name='requirements.txt'):
    """Get requirements as a list."""

    path = os.path.join(get_app_directory(), file_name)
    requirements_list = []

    if os.path.exists(path):
        requirements_list = [str(r.req) for r in req.parse_requirements(
            path,
            session=False
        )]

    if 'develop' in sys.argv and file_name == 'requirements.txt':
        requirements_list += get_requirements(
            file_name='requirements.develop.txt'
        )

    return requirements_list


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
    description = ""

    if os.path.exists(path):
        with open(path) as in_file:
            description = in_file.read()

    return description

arguments = {
    'name': 'confectionary-confetti',
    'version': '0.1',
    'license': 'Other/Proprietary License',
    'long_description': get_description(),
    'description': __doc__,
    'install_requires': get_requirements(),
    'dependency_links': get_dependency_links(),
    'packages': find_packages(),
}

setup(**arguments)
