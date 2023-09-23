import os
from datetime import datetime

import boto3
from tools import get_event_timestamp


class AppRunner:
    def __init__(self):
        self.apprunner_client = boto3.client("apprunner")

    def list_resources(self, action: str, selector: str):
        """
        Get all AppRunner services in the account and return them as a list

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

        print(">> Listing AppRunner services")

        while params.get("NextToken") != "":
            list_response = self.apprunner_client.list_services(**params)

            if len(list_response["ServiceSummaryList"]) != 0:
                for service in list_response["ServiceSummaryList"]:
                    tags_list = self.apprunner_client.list_tags_for_resource(ResourceArn=service["ServiceArn"])["Tags"]

                    service_event_time = get_event_timestamp(
                        [{"key": tag["Key"], "value": tag["Value"]} for tag in tags_list], action, selector
                    )

                    resource_details = {
                        "resourceArn": service["ServiceArn"],
                        "details": {"ServiceId": service["ServiceId"], "ServiceName": service["ServiceName"]},
                        "nextEventTime": service_event_time,
                    }

                    if service_event_time:
                        print(f">> App Runner {service['ServiceName']} will {action} on {service_event_time}")

                        payload.append(resource_details)
                    else:
                        print(
                            f">> No {action} event for App Runner {service['ServiceName']} in the next {os.environ.get('EXECUTION_INTERVAL')} hours"
                        )

                params["NextToken"] = list_response.get("NextToken", "")
            else:
                break

        payload = sorted(payload, key=lambda x: x["nextEventTime"])

        return payload
