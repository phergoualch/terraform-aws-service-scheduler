import logging
from typing import Dict, List

from models import Resource, Tag, Service
from models.enums import Action


logger = logging.getLogger(__name__)


class Elasticache(Service):
    def __init__(self, action: Action, parameters: Dict = None):
        super().__init__("elasticache", action, parameters)

    def list_resources(self) -> List[Resource]:
        """
        Get all Elasticache clusters in the account and return them as a list of Resource objects.

        Returns
        -------
        resources : List[Resource]
        """
        resources = []
        paginator = self.client.get_paginator("describe_cache_clusters")

        logger.info("Listing Elasticache clusters")

        try:
            for page in paginator.paginate():
                for cluster in page["CacheClusters"]:
                    try:
                        account_id = self.sts.get_caller_identity()["Account"]
                        region = self.client.meta.region_name
                        cluster_arn = f"arn:aws:elasticache:{region}:{account_id}:cluster:{cluster['CacheClusterId']}"
                        tags = self.client.list_tags_for_resource(ResourceName=cluster_arn)

                        target_node_type = [
                            tag["Value"] for tag in tags["TagList"] if tag["Key"] == self.get_tag_key("node-type", action=self.action)
                        ][0]
                    except Exception as e:
                        logger.warning(f"Error listing tags for Elasticache cluster {cluster['CacheClusterId']}: {e}")
                        continue

                    resources.append(
                        Resource(
                            id_=cluster_arn,
                            service=self,
                            tags=[Tag(tag["Key"], tag["Value"]) for tag in tags["TagList"]],
                            attributes={"id": cluster["CacheClusterId"], "nodeType": target_node_type},
                        )
                    )
            logger.info(f"Found {len(resources)} Elasticache clusters")
            return resources

        except Exception as e:
            logger.error(f"Error listing Elasticache clusters: {e}")
            raise e
