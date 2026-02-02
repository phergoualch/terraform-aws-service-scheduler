import logging

from models import Resource, Service, Tag
from models.enums import Action

logger = logging.getLogger(__name__)


class Redshift(Service):
    def __init__(self, action: Action, parameters: dict | None = None):
        super().__init__("redshift", action, parameters)

    def list_resources(self) -> list[Resource]:
        """
        Get all Redshift clusters in the account and return them as a list of Resource objects.

        Returns
        -------
        resources : List[Resource]
        """
        resources = []
        paginator = self.client.get_paginator("describe_clusters")

        logger.info("Listing Redshift clusters")

        try:
            for page in paginator.paginate():
                for cluster in page["Clusters"]:
                    resources.append(
                        Resource(
                            id_=cluster["ClusterIdentifier"],
                            service=self,
                            tags={
                                Tag(tag["Key"], tag["Value"])
                                for tag in cluster.get("Tags", [])
                            },
                            attributes={"name": cluster["ClusterIdentifier"]},
                        )
                    )

            logger.info(f"Found {len(resources)} Redshift clusters")

        except Exception as e:
            logger.error(f"Error listing Redshift clusters: {e}")
            raise e

        return resources
