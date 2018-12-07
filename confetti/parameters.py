"""Parameters."""
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
    def get_parameters(client, **kwargs):
        """Get a dictionary of parameters."""
        generator = ClientResponseGenerator(client)
        args = ["get_parameters_by_path", "Parameters"]

        return generator.get(*args, **kwargs)

    def __init__(
        self,
        session=None,
        confetti_key=None,
        confetti_path=None,
        **kwargs
    ):
        """Override init method."""
        if session:
            self.session = session
        else:
            self.session = boto3.session.Session()

        if confetti_key:
            self.confetti_key = confetti_key
        else:
            self.confetti_key = os.getenv("CONFETTI_KEY", "Development")

        if confetti_path:
            self.confetti_path = confetti_path
        else:
            confetti_path = self.__class__.__name__
            self.confetti_path = os.getenv("CONFETTI_PATH", confetti_path)

        self.kwargs = kwargs
        self.kwargs["Path"] = os.path.join(
            "/",
            self.confetti_key,
            self.confetti_path
        )

        if "WithDecryption" not in self.kwargs.keys():
            self.kwargs["WithDecryption"] = True

    def __str__(self):
        """Override __str__ method."""
        return f"{self.kwargs}"

    def get(self):
        """Get namespaced parameters."""
        client = self.session.client("ssm")
        parameters = dict()

        for parameter in self.get_parameters(client, **self.kwargs):
            name = os.path.basename(parameter["Name"])
            value = parameter["Value"]

            parameters[name] = value

        return SimpleNamespace(**parameters)

    def set(self, file_name):
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
                    print(f"{parameter_already_exists}: {parameter}")
                else:
                    raise e

    def export_parameters(self, file_name):
        """Export parameters."""
        client = self.session.client("ssm")
        parameters = list()

        for parameter in self.get_parameters(client, **self.kwargs):
            parameters.append({
                "Name": os.path.basename(parameter["Name"]),
                "Value": parameter["Value"],
                "Type": parameter["Type"],
                "Overwrite": True
            })

        with open(file_name, "w") as out_file:
            json.dump(parameters, out_file)
