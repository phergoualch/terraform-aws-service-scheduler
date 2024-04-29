import logging
from typing import Dict, List

from models import Resource, Tag, Service
from models.enums import Action


logger = logging.getLogger(__name__)


class Aurora(Service):
    def __init__(self, action: Action, parameters: Dict = None):
        super().__init__("rds", action, parameters)

    def list_resources(self) -> List[Resource]:
        """
        Get all Aurora clusters in the account and return them as a list of Resource objects.

        Returns
        -------
        resources : List[Resource]
        """
        resources = []
        paginator = self.client.get_paginator("describe_db_clusters")

        logger.info("Listing Aurora clusters")

        try:
            for page in paginator.paginate(
                Filters=[{"Name": "engine", "Values": ["aurora-postgresql", "aurora-mysql"]}]
            ):
                for cluster in page["DBClusters"]:
                    try:
                        tags = self.client.list_tags_for_resource(
                            ResourceName=cluster["DBClusterArn"]
                        )
                    except Exception as e:
                        logger.warning(
                            f"Error listing tags for Aurora cluster {cluster['DBClusterArn']}: {e}"
                        )
                        continue

                    resources.append(
                        Resource(
                            id_=cluster["DBClusterArn"],
                            service=self,
                            tags=set([Tag(tag["Key"], tag["Value"]) for tag in tags["TagList"]]),
                            attributes={"name": cluster["DBClusterIdentifier"]},
                        )
                    )

            logger.info(f"Found {len(resources)} Aurora clusters")

        except Exception as e:
            logger.error(f"Error listing Aurora clusters: {e}")
            raise e

        return resources
