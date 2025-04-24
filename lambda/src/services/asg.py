import logging
from typing import Dict, List

from models import Resource, Tag, Service
from models.enums import Action

logger = logging.getLogger(__name__)


class ASG(Service):
    def __init__(self, action: Action, parameters: Dict = None):
        super().__init__("asg", action, parameters, "autoscaling")

    def list_resources(self) -> List[Resource]:
        """
        Get all Autoscaling Groups in the account and return them as a list of Resource objects.

        Returns
        -------
        resources : List[Resource]
        """
        resources = []
        paginator = self.client.get_paginator("describe_auto_scaling_groups")

        logger.info("Listing Autoscaling Groups")

        try:
            for page in paginator.paginate(
                Filters=[
                    {"Name": f"tag:{self.get_tag_key('enabled')}", "Values": ["true"]}
                ]
            ):
                for group in page["AutoScalingGroups"]:
                    resources.append(
                        Resource(
                            id_=group["AutoScalingGroupARN"],
                            service=self,
                            tags=set(
                                [
                                    Tag(tag["Key"], tag["Value"])
                                    for tag in group.get("Tags", [])
                                ]
                            ),
                            attributes={"name": group["AutoScalingGroupName"]},
                        )
                    )

            logger.info(f"Found {len(resources)} Autoscaling Groups")
            return resources

        except Exception as e:
            logger.error(f"Error listing EC2 instances: {e}")
            raise e
