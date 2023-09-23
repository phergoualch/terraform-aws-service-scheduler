import os
from datetime import datetime

import boto3
from tools import get_event_timestamp


class ASG:
    def __init__(self):
        self.autoscaling_client = boto3.client("autoscaling")

    def list_resources(self, action: str, selector: str):
        """
        Get all EC2 autoscaling in the account and return them as a list

        Parameters
        ----------
        action : str
            The action of the event (start or stop)
        selector : str
            The tags selector in case of manual action

        Returns
        -------
        resources : List[Dict]
        """
        payload = []
        params = {}

        print(">> Listing EC2 autoscaling groups")

        while params.get("nextToken") != "":
            describe_response = self.autoscaling_client.describe_auto_scaling_groups(
                Filters=[{"Name": "tag:finops:enabled", "Values": ["true"]}], **params
            )

            if len(describe_response["AutoScalingGroups"]) != 0:
                for group in describe_response["AutoScalingGroups"]:
                    group_event_time = get_event_timestamp(
                        [{"key": tag["Key"], "value": tag["Value"]} for tag in group["Tags"]], action, selector
                    )

                    resource_details = {
                        "resourceArn": group["AutoScalingGroupARN"],
                        "details": {"groupName": group["AutoScalingGroupName"]},
                        "resourceTtl": str(int(datetime.now().timestamp()) + 60 * 60 * 24 * 30),
                        "nextEventTime": group_event_time,
                    }

                    if group_event_time:
                        print(
                            f">> Autoscaling group {group['AutoScalingGroupName']} will {action} on {group_event_time}"
                        )

                        payload.append(resource_details)
                    else:
                        print(
                            f">> No {action} event for autoscaling group {group['AutoScalingGroupName']} in the next {os.environ.get('EXECUTION_INTERVAL')} hours"
                        )

                params["nextToken"] = describe_response.get("nextToken", "")
            else:
                break

        payload = sorted(payload, key=lambda x: x["nextEventTime"])

        return payload
