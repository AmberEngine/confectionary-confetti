"""Confetti."""
import os

from pip.req import parse_requirements
from setuptools import setup, find_packages

requirements = os.path.join(os.path.dirname(__file__), 'requirements.txt')
install_requires = [
    str(r.req) for r in parse_requirements(requirements, session=False)
]

setup(
    name='confectionary-confetti',
    version='0.1',
    description=__doc__,
    packages=find_packages(),
    install_requires=install_requires
)
