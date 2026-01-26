import logging

from models import Resource, Service, Tag
from models.enums import Action

logger = logging.getLogger(__name__)


class Cloudwatch(Service):
    def __init__(self, action: Action, parameters: dict | None = None):
        super().__init__("cloudwatch", action, parameters)

    def list_resources(self) -> list[Resource]:
        """
        Get all Cloudwatch alarms in the account and return them as a list of Resource objects.

        Returns
        -------
        resources : List[Resource]
        """
        resources = []
        paginator = self.client.get_paginator("describe_alarms")

        logger.info("Listing Cloudwatch alarms")

        try:
            for page in paginator.paginate(
                AlarmTypes=["CompositeAlarm", "MetricAlarm"]
            ):
                for alarm in page["MetricAlarms"] + page["CompositeAlarms"]:
                    try:
                        tags = self.client.list_tags_for_resource(
                            ResourceARN=alarm["AlarmArn"]
                        )
                    except Exception as e:
                        logger.warning(
                            f"Error listing tags for Cloudwatch alarm {alarm['AlarmArn']}: {e}"
                        )
                        continue

                    resources.append(
                        Resource(
                            id_=alarm["AlarmArn"],
                            service=self,
                            tags={
                                Tag(tag["Key"], tag["Value"])
                                for tag in tags.get("Tags", [])
                            },
                            attributes={"name": alarm["AlarmName"]},
                        )
                    )
            logger.info(f"Found {len(resources)} Cloudwatch alarms")
            return resources

        except Exception as e:
            logger.error(f"Error listing Cloudwatch alarms: {e}")
            raise e
