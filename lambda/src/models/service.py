import os
from datetime import datetime
from dateutil import tz
from typing import Dict
import json

import boto3
from models.enums import Action


class Service:
    """
    Represents a service.

    Attributes
    ----------
    name : str
        The name of the service.
    client : boto3.client
        The boto3 client for the service.
    action : Action
        The action associated with the service.
    now : datetime
        The current datetime.

    Methods
    -------
    __repr__()
        Return a string representation of the service.
    get_tag_key(tag_name, action)
        Get the tag key from the tag mapping.
    """

    def __init__(self, name: str, action: Action, parameters: Dict = None, client_name: str = None):
        """
        Initialize a Service instance.

        Parameters
        ----------
        name : str
            The name of the service.
        action : Action
            The action associated with the service.
        parameters : Dict, optional
            Additional parameters, by default None.
        client_name : str, optional
            The name of the boto3 client, if different from the service name, by default None.
        """
        self.name = name
        if client_name:
            self.client = boto3.client(client_name)
        else:
            self.client = boto3.client(name)
        self.action = action
        self.now = datetime.now(tz=tz.gettz("UTC"))

        self.ssm = boto3.client("ssm")
        self.sts = boto3.client("sts")

        if parameters:
            self.tags_prefix = parameters.get("tags_prefix")
            self.tags_mapping = parameters.get("tags_mapping")
            self.interval = int(parameters.get("interval"))
            self.default_timezone = parameters.get("default_timezone")
        else:
            self.tags_prefix = os.environ.get("TAGS_PREFIX")
            self.tags_mapping = json.loads(os.environ.get("TAGS_MAPPING"))
            self.interval = int(os.environ.get("EXECUTION_INTERVAL"))
            self.default_timezone = os.environ.get("DEFAULT_TIMEZONE")

    def __repr__(self):
        """
        Return a string representation of the service.

        Returns
        -------
        str
            A string representation of the service.
        """
        return f"Service(name={self.name}, action={self.action})"

    def get_tag_key(self, tag_name: str, action: bool = False, iterator: int = None):
        """
        Get the tag key from the tag mapping.

        Parameters
        ----------
        tag_name : str
            The name of the tag.
        action : bool, optional
            Whether to include the action in the tag key, by default False.
        iterator : int, optional
            The iterator, by default None.

        Returns
        -------
        str
            The tag key.
        """
        if action and iterator:
            return f"{self.tags_prefix}:{self.action.value}-{self.tags_mapping[tag_name]}:{iterator}"
        elif action:
            return f"{self.tags_prefix}:{self.action.value}-{self.tags_mapping[tag_name]}"
        elif iterator:
            return f"{self.tags_prefix}:{self.tags_mapping[tag_name]}:{iterator}"
        else:
            return f"{self.tags_prefix}:{self.tags_mapping[tag_name]}"
