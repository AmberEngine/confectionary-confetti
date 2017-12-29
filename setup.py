"""Confetti."""
from setuptools import setup, find_packages

install_requires = []
tests_require = install_requires +['boto3==1.5', 'pytest==3.2.3']

setup(
    name='confectionary-confetti',
    version='0.1',
    description=__doc__,
    packages=find_packages(),
    py_modules=['confetti'],
    install_requires=install_requires,
    tests_require=tests_require
)
