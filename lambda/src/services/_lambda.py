import os

import boto3
from tools import get_event_timestamp


class Lambda:
    def __init__(self):
        self.lambda_client = boto3.client("lambda")

    def list_resources(self, action: str, selector: str):
        """
        Get all Lambda functions in the account and return them as a list

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

        print(">> Listing Lambda functions")

        while params.get("Marker") != "":
            describe_response = self.lambda_client.list_functions(**params)

            if len(describe_response["Functions"]) != 0:
                for function in describe_response["Functions"]:
                    tags = self.lambda_client.list_tags(Resource=function["FunctionArn"])

                    function_event_time = get_event_timestamp(
                        [{"key": tag, "value": tags["Tags"][tag]} for tag in tags["Tags"]], action, selector
                    )

                    resource_details = {
                        "resourceArn": function["FunctionArn"],
                        "details": {"functionName": function["FunctionName"]},
                        "nextEventTime": function_event_time,
                    }

                    if function_event_time:
                        print(f">> Lambda function {function['FunctionName']} will {action} on {function_event_time}")

                        payload.append(resource_details)
                    else:
                        print(
                            f">> No {action} event for Lambda function {function['FunctionName']} in the next {os.environ.get('EXECUTION_INTERVAL')} hours"
                        )
                params["Marker"] = describe_response.get("NextMarker", "")
            else:
                break

        payload = sorted(payload, key=lambda x: x["nextEventTime"])

        return payload
