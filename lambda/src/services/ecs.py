import logging
from typing import Dict, List

from models import Resource, Tag, Service
from models.enums import Action


logger = logging.getLogger(__name__)


class ECS(Service):
    def __init__(self, action: Action, parameters: Dict = None):
        super().__init__("ecs", action, parameters)

    def list_resources(self) -> List[Resource]:
        """
        Get all ECS services in the account and return them as a list of Resource objects.

        Returns
        -------
        resources : List[Resource]
        """
        resources = []
        clusters_paginator = self.client.get_paginator("list_clusters")

        logger.info("Listing ECS services")

        try:
            for cluster_page in clusters_paginator.paginate():
                for cluster_arn in cluster_page["clusterArns"]:
                    services_paginator = self.client.get_paginator("list_services")
                    for service_page in services_paginator.paginate(cluster=cluster_arn):
                        for service_arn in service_page["serviceArns"]:
                            try:
                                tags = self.client.list_tags_for_resource(resourceArn=service_arn)
                            except Exception as e:
                                logger.warning(f"Error listing tags for ECS service {service_arn}: {e}")
                                continue

                            resources.append(
                                Resource(
                                    id_=service_arn,
                                    service=self,
                                    tags=[Tag(tag["key"], tag["value"]) for tag in tags["tags"]],
                                    attributes={
                                        "cluster": cluster_arn.split("/")[-1],
                                        "service": service_arn.split("/")[-1],
                                    },
                                )
                            )

            logger.info(f"Found {len(resources)} ECS services")
            return resources

        except Exception as e:
            logger.error(f"Error listing ECS services: {e}")
            raise e
