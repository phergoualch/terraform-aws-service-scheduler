import logging
from typing import Dict, List

from models import Resource, Tag, Service
from models.enums import Action

logger = logging.getLogger(__name__)


class AppRunner(Service):
    def __init__(self, action: Action, parameters: Dict = None):
        super().__init__("apprunner", action, parameters)

    def list_resources(self) -> List[Resource]:
        """
        Get all AppRunner services in the account and return them as a list of Resource objects.

        Returns
        -------
        resources : List[Resource]
        """
        resources = []
        params = {}

        logger.info("Listing AppRunner services")

        try:
            while True:
                response = self.client.list_services(**params)

                for service in response["ServiceSummaryList"]:
                    try:
                        tags = self.client.list_tags_for_resource(ResourceArn=service["ServiceArn"])
                    except Exception as e:
                        logger.warning(f"Error listing tags for AppRunner service {service['ServiceArn']}: {e}")
                        continue

                    resources.append(
                        Resource(
                            id_=service["ServiceArn"], service=self, tags=[Tag(tag["Key"], tag["Value"]) for tag in tags.get("Tags", [])]
                        )
                    )

                params["NextToken"] = response.get("NextToken")
                if not params["NextToken"]:
                    break

            logger.info(f"Found {len(resources)} AppRunner services")
            return resources

        except Exception as e:
            logger.error(f"Error listing AppRunner services: {e}")
            raise e
