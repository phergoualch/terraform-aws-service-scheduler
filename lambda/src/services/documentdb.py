import logging
from typing import Dict, List

from models import Resource, Tag, Service
from models.enums import Action


logger = logging.getLogger(__name__)


class DocumentDB(Service):
    def __init__(self, action: Action, parameters: Dict = None):
        super().__init__("docdb", action, parameters)

    def list_resources(self) -> List[Resource]:
        """
        Get all DocumentDB clusters in the account and return them as a list of Resource objects.

        Returns
        -------
        resources : List[Resource]
        """
        resources = []
        paginator = self.client.get_paginator("describe_db_clusters")

        logger.info("Listing DocumentDB clusters")

        try:
            for page in paginator.paginate(Filters=[{"Name": "engine", "Values": ["docdb"]}]):
                for cluster in page["DBClusters"]:
                    try:
                        tags = self.client.list_tags_for_resource(
                            ResourceName=cluster["DBClusterArn"]
                        )
                    except Exception as e:
                        logger.warning(
                            f"Error listing tags for DocumentDB cluster {cluster['DBClusterArn']}: {e}"
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

            logger.info(f"Found {len(resources)} DocumentDB clusters")
            return resources

        except Exception as e:
            logger.error(f"Error listing DocumentDB clusters: {e}")
            raise e
