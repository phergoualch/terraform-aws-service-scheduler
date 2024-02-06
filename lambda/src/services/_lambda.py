import logging
from typing import Dict, List

from models import Resource, Tag, Service
from models.enums import Action

logger = logging.getLogger(__name__)


class Lambda(Service):
    def __init__(self, action: Action, parameters: Dict = None):
        super().__init__("lambda", action, parameters)

    def list_resources(self) -> List[Resource]:
        """
        Get all Lambda functions in the account and return them as a list of Resource objects.

        Returns
        -------
        resources : List[Resource]
        """
        resources = []
        paginator = self.client.get_paginator("list_functions")

        logger.info("Listing Lambda functions")

        try:
            for page in paginator.paginate():
                for function in page["Functions"]:
                    try:
                        tags = self.client.list_tags(Resource=function["FunctionArn"])
                    except Exception as e:
                        logger.warning(f"Error listing tags for Lambda function {function['FunctionArn']}: {e}")
                        continue

                    resources.append(
                        Resource(
                            id_=function["FunctionArn"],
                            service=self,
                            tags=[Tag(tag, tags["Tags"][tag]) for tag in tags["Tags"]],
                            attributes={"name": function["FunctionName"]},
                        )
                    )

            logger.info(f"Found {len(resources)} Lambda functions")
            return resources

        except Exception as e:
            logger.error(f"Error listing Lambda functions: {e}")
            raise e
