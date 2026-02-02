import logging

from models import Resource, Service, Tag
from models.enums import Action

logger = logging.getLogger(__name__)


class SageMakerEndpoint(Service):
    def __init__(self, action: Action, parameters: dict | None = None):
        super().__init__("sagemaker", action, parameters)

    def list_resources(self) -> list[Resource]:
        """
        Get all SageMaker Endpoints in the account and return them as a list of Resource objects.

        Returns
        -------
        resources : List[Resource]
        """
        resources = []
        paginator = self.client.get_paginator("list_endpoints")

        logger.info("Listing SageMaker Endpoints")

        try:
            for page in paginator.paginate():
                for endpoint in page["Endpoints"]:
                    try:
                        tags = self.client.list_tags(
                            ResourceArn=endpoint["EndpointArn"]
                        )
                    except Exception as e:
                        logger.warning(
                            f"Error listing tags for SageMaker Endpoint {endpoint['EndpointArn']}: {e}"
                        )
                        continue

                    resources.append(
                        Resource(
                            id_=endpoint["EndpointArn"],
                            service=self,
                            tags={
                                Tag(tag["Key"], tag["Value"])
                                for tag in tags.get("Tags", [])
                            },
                            attributes={"name": endpoint["EndpointName"]},
                        )
                    )

            logger.info(f"Found {len(resources)} SageMaker Endpoints")

        except Exception as e:
            logger.error(f"Error listing SageMaker Endpoints: {e}")
            raise e

        return resources
