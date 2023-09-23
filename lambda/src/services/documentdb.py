import os

import boto3
from tools import get_event_timestamp


class DocumentDB:
    def __init__(self):
        self.documentdb_client = boto3.client("docdb")

    def list_resources(self, action: str, selector: str):
        """
        Get all DocumentDB clusters in the account and return them as a list

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

        print(">> Listing DocumentDB clusters")

        while params.get("Marker") != "":
            describe_response = self.documentdb_client.describe_db_clusters(
                Filters=[{"Name": "engine", "Values": ["docdb"]}], **params
            )

            if len(describe_response["DBClusters"]) != 0:
                for cluster in describe_response["DBClusters"]:
                    tags = self.documentdb_client.list_tags_for_resource(ResourceName=cluster["DBClusterArn"])

                    cluster_event_time = get_event_timestamp(
                        [{"key": tag["Key"], "value": tag["Value"]} for tag in tags["TagList"]], action, selector
                    )

                    resource_details = {
                        "resourceArn": cluster["DBClusterArn"],
                        "details": {"clusterIdentifier": cluster["DBClusterIdentifier"]},
                        "nextEventTime": cluster_event_time,
                    }

                    if cluster_event_time:
                        print(
                            f">> DocumentDB cluster {cluster['DBClusterIdentifier']} will {action} on {cluster_event_time}"
                        )

                        payload.append(resource_details)
                    else:
                        print(
                            f">> No {action} event for DocumentDB cluster {cluster['DBClusterIdentifier']} in the next {os.environ.get('EXECUTION_INTERVAL')} hours"
                        )

                params["Marker"] = describe_response.get("Marker", "")
            else:
                break

        payload = sorted(payload, key=lambda x: x["nextEventTime"])

        return payload
