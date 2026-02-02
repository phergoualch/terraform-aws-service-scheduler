import logging

from models import Resource, Service, Tag
from models.enums import Action

logger = logging.getLogger(__name__)


class Neptune(Service):
    def __init__(self, action: Action, parameters: dict | None = None):
        super().__init__("neptune", action, parameters)

    def list_resources(self) -> list[Resource]:
        """
        Get all Neptune clusters in the account and return them as a list of Resource objects.

        Returns
        -------
        resources : List[Resource]
        """
        resources = []
        paginator = self.client.get_paginator("describe_db_clusters")

        logger.info("Listing Neptune clusters")

        try:
            for page in paginator.paginate(
                Filters=[{"Name": "engine", "Values": ["neptune"]}]
            ):
                for cluster in page["DBClusters"]:
                    try:
                        tags = self.client.list_tags_for_resource(
                            ResourceName=cluster["DBClusterArn"]
                        )
                    except Exception as e:
                        logger.warning(
                            f"Error listing tags for Neptune cluster {cluster['DBClusterArn']}: {e}"
                        )
                        continue

                    resources.append(
                        Resource(
                            id_=cluster["DBClusterArn"],
                            service=self,
                            tags={
                                Tag(tag["Key"], tag["Value"])
                                for tag in tags.get("TagList", [])
                            },
                            attributes={"name": cluster["DBClusterIdentifier"]},
                        )
                    )

            logger.info(f"Found {len(resources)} Neptune clusters")

        except Exception as e:
            logger.error(f"Error listing Neptune clusters: {e}")
            raise e

        return resources
