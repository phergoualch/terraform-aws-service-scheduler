import os
from datetime import datetime

import boto3
from tools import get_event_timestamp


class EC2:
    def __init__(self):
        self.ec2_client = boto3.client("ec2")

    def list_resources(self, action: str, selector: str):
        """
        Get all EC2 without autoscaling in the account and return them as a list

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

        print(">> Listing EC2 instances")

        while params.get("nextToken") != "":
            describe_response = self.ec2_client.describe_instances(
                Filters=[{"Name": "tag:finops:enabled", "Values": ["true"]}], **params
            )

            if len(describe_response["Reservations"]) != 0:
                for r in describe_response["Reservations"]:
                    for instance in r["Instances"]:
                        instance_event_time = get_event_timestamp(
                            [{"key": tag["Key"], "value": tag["Value"]} for tag in instance["Tags"]], action, selector
                        )

                        resource_details = {
                            "details": {"instanceID": [instance["InstanceId"]]},
                            "nextEventTime": instance_event_time,
                        }

                        if instance_event_time:
                            print(f">> EC2 instance {instance['InstanceId']} will {action} on {instance_event_time}")

                            payload.append(resource_details)

                        else:
                            print(
                                f">> No {action} event for EC2 instance {instance['InstanceId']} in the next {os.environ.get('EXECUTION_INTERVAL')} hours"
                            )

                params["nextToken"] = describe_response.get("nextToken", "")
            else:
                break

        payload = sorted(payload, key=lambda x: x["nextEventTime"])

        return payload
