import logging

from models import Resource, Service, Tag
from models.enums import Action

logger = logging.getLogger(__name__)


class SageMakerNotebook(Service):
    def __init__(self, action: Action, parameters: dict | None = None):
        super().__init__("sagemaker", action, parameters)

    def list_resources(self) -> list[Resource]:
        """
        Get all SageMaker Notebook Instances in the account and return them as a list of Resource objects.

        Returns
        -------
        resources : List[Resource]
        """
        resources = []
        paginator = self.client.get_paginator("list_notebook_instances")

        logger.info("Listing SageMaker Notebook Instances")

        try:
            for page in paginator.paginate():
                for notebook in page["NotebookInstances"]:
                    try:
                        tags = self.client.list_tags(
                            ResourceArn=notebook["NotebookInstanceArn"]
                        )
                    except Exception as e:
                        logger.warning(
                            f"Error listing tags for SageMaker Notebook {notebook['NotebookInstanceArn']}: {e}"
                        )
                        continue

                    resources.append(
                        Resource(
                            id_=notebook["NotebookInstanceArn"],
                            service=self,
                            tags={
                                Tag(tag["Key"], tag["Value"])
                                for tag in tags.get("Tags", [])
                            },
                            attributes={"name": notebook["NotebookInstanceName"]},
                        )
                    )

            logger.info(f"Found {len(resources)} SageMaker Notebook Instances")

        except Exception as e:
            logger.error(f"Error listing SageMaker Notebook Instances: {e}")
            raise e

        return resources
