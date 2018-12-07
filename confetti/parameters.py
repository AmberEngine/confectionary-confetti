"""AWS SSM parameter store utility."""
import json
import os

from types import SimpleNamespace

import boto3
import botocore

from confetti.utils.kms import ensure_key
from confetti.utils.client import ClientResponseGenerator


class Confetti:
    """Base class for Confetti."""

    @staticmethod
    def get_session(session=None):
        """Get the default session if none is set."""
        if not session:
            session = boto3.session.Session()

        return session

    @staticmethod
    def get_confetti_key(confetti_key=None):
        """Get the default confetti_key if none is set."""
        if not confetti_key:
            confetti_key = os.getenv("CONFETTI_KEY", "Development")

        return confetti_key

    @classmethod
    def get_confetti_path(cls, confetti_path=None):
        """Get the default confetti_path if none is set."""
        if not confetti_path:
            class_name = cls.__name__
            confetti_path = os.getenv("CONFETTI_PATH", class_name)

        return confetti_path

    @staticmethod
    def get_path(confetti_key, confetti_path):
        """Get the constructed path for AWS SSM parameter store."""
        return os.path.join("/", confetti_key, confetti_path)

    def __init__(self, session=None, confetti_key=None, confetti_path=None):
        """Override init method."""
        self.session = self.get_session(session)
        self.confetti_key = self.get_confetti_key(confetti_key)
        self.confetti_path = self.get_confetti_path(confetti_path)
        self.path = self.get_path(self.confetti_key, self.confetti_path)

    def __repr__(self):
        """Override repr method."""
        return(
            f"{self.__class__.__name__}("
            f"session={self.session}, "
            f"confetti_key={'self.confetti_key'}, "
            f"confetti_path={'self.confetti_path'})"
        )

    def __str__(self):
        """Override str method."""
        return f"{self.path}"

    def get_parameters_by_path(self, **kwargs):
        """Get a dictionary of parameters."""
        client = self.session.client("ssm")
        generator = ClientResponseGenerator(client)
        kwargs["Path"] = self.path

        if "WithDecryption" not in kwargs.keys():
            kwargs["WithDecryption"] = True

        return generator.get("get_parameters_by_path", "Parameters", **kwargs)

    def get_parameters(self, **kwargs):
        """Get namespaced parameters."""
        parameters = dict()

        for parameter in self.get_parameters_by_path(**kwargs):
            name = os.path.basename(parameter["Name"])
            value = parameter["Value"]

            parameters[name] = value

        return SimpleNamespace(**parameters)

    def export_parameters(self, file_name, **kwargs):
        """Export parameters."""
        parameters = list()

        for parameter in self.get_parameters_by_path(**kwargs):
            parameters.append({
                "Name": os.path.basename(parameter["Name"]),
                "Value": parameter["Value"],
                "Type": parameter["Type"],
                "Overwrite": True
            })

        with open(file_name, "w") as out_file:
            json.dump(parameters, out_file)

    def import_parameters(self, file_name):
        """Set parameters."""
        client = self.session.client("ssm")
        key = os.path.join("alias", self.confetti_key)
        path = os.path.join("/", self.confetti_key, self.confetti_path)
        parameters = list()

        with open(file_name) as in_file:
            parameters = json.load(in_file)

        ensure_key(self.session.client("kms"), key)

        for parameter in parameters:
            parameter["Name"] = os.path.join(path, parameter["Name"])

            if not parameter.get("Type"):
                parameter["Type"] = "String"
            elif parameter["Type"] == "SecureString":
                parameter["KeyId"] = key

            try:
                client.put_parameter(**parameter)
            except botocore.exceptions.ClientError as e:
                parameter_already_exists = "ParameterAlreadyExists"

                if e.response["Error"]["Code"] == parameter_already_exists:
                    pass
                else:
                    raise e
