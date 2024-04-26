import logging
from typing import Dict, List

from models import Resource, Tag, Service
from models.enums import Action


logger = logging.getLogger(__name__)


class EC2(Service):
    def __init__(self, action: Action, parameters: Dict = None):
        super().__init__("ec2", action, parameters)

    def list_resources(self) -> List[Resource]:
        """
        Get all EC2 instances in the account and return them as a list of Resource objects.

        Returns
        -------
        resources : List[Resource]
        """
        resources = []
        paginator = self.client.get_paginator("describe_instances")

        logger.info("Listing EC2 instances")

        try:
            for page in paginator.paginate():
                for reservation in page["Reservations"]:
                    for instance in reservation["Instances"]:
                        if instance["State"]["Name"] != "terminated":
                            resources.append(
                                Resource(
                                    id_=instance["InstanceId"],
                                    service=self,
                                    tags=set(
                                        [Tag(tag["Key"], tag["Value"]) for tag in instance["Tags"]]
                                    ),
                                )
                            )
            logger.info(f"Found {len(resources)} EC2 instances")
            return resources

        except Exception as e:
            logger.error(f"Error listing EC2 instances: {e}")
            raise e
