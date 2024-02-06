import logging
from typing import Dict, List

from models import Resource, Tag, Service
from models.enums import Action


logger = logging.getLogger(__name__)


class RDS(Service):
    def __init__(self, action: Action, parameters: Dict = None):
        super().__init__("rds", action, parameters)

    def list_resources(self) -> List[Resource]:
        """
        Get all RDS instances in the account and return them as a list of Resource objects.

        Returns
        -------
        resources : List[Resource]
        """
        resources = []
        paginator = self.client.get_paginator("describe_db_instances")

        logger.info("Listing RDS instances")

        try:
            for page in paginator.paginate():
                for instance in page["DBInstances"]:
                    try:
                        tags = self.client.list_tags_for_resource(ResourceName=instance["DBInstanceArn"])
                    except Exception as e:
                        logger.warning(f"Error listing tags for RDS instance {instance['DBInstanceArn']}: {e}")
                        continue

                    resources.append(
                        Resource(
                            id_=instance["DBInstanceArn"],
                            service=self,
                            tags=[Tag(tag["Key"], tag["Value"]) for tag in tags["TagList"]],
                            attributes={"name": instance["DBInstanceIdentifier"]},
                        )
                    )

            logger.info(f"Found {len(resources)} RDS instances")

        except Exception as e:
            logger.error(f"Error listing RDS instances: {e}")
            raise e

        return resources
