import os

import boto3
from tools import get_event_timestamp


class RDS:
    def __init__(self):
        self.rds_client = boto3.client("rds")

    def list_resources(self, action: str, selector: str):
        """
        Get all Aurora clusters and RDS instances in the account and return them as a list

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

        print(">> Listing Aurora clusters and RDS instances")

        clusters = self.list_clusters(action=action, selector=selector)
        instances = self.list_instances(action=action, selector=selector)

        payload = clusters + instances

        return sorted(payload, key=lambda x: x["nextEventTime"])

    def list_clusters(self, action: str, selector: str):
        """
        Get all Aurora clusters in the account and return them as a list

        Parameters
        ----------
        action : str
            The action of the event (start or stop)
        selector : str
            The tags selector in case of manual action

        Returns
        -------
        clusters : List[Dict]
        """
        payload = []
        params = {}

        while params.get("Marker") != "":
            describe_response = self.rds_client.describe_db_clusters(
                Filters=[{"Name": "engine", "Values": ["aurora-postgresql", "aurora-mysql"]}],
                **params,
            )

            if len(describe_response["DBClusters"]) != 0:
                for cluster in describe_response["DBClusters"]:
                    tags = self.rds_client.list_tags_for_resource(ResourceName=cluster["DBClusterArn"])

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
                            f">> Aurora cluster {cluster['DBClusterIdentifier']} will {action} on {cluster_event_time}"
                        )

                        payload.append(resource_details)
                    else:
                        print(
                            f">> No {action} event for Aurora cluster {cluster['DBClusterIdentifier']} in the next {os.environ.get('EXECUTION_INTERVAL')} hours"
                        )

                params["Marker"] = describe_response.get("Marker", "")
            else:
                break

        return payload

    def list_instances(self, action: str, selector: str):
        """
        Get all RDS instances in the account and return them as a list

        Parameters
        ----------
        action : str
            The action of the event (start or stop)
        selector : str
            The tags selector in case of manual action

        Returns
        -------
        instances : List[Dict]
        """
        payload = []
        params = {}

        while params.get("Marker") != "":
            describe_response = self.rds_client.describe_db_instances(**params)

            if len(describe_response["DBInstances"]) != 0:
                for instance in describe_response["DBInstances"]:
                    if instance.get("DBClusterIdentifier"):
                        continue

                    tags = self.rds_client.list_tags_for_resource(ResourceName=instance["DBInstanceArn"])

                    instance_event_time = get_event_timestamp(
                        [{"key": tag["Key"], "value": tag["Value"]} for tag in tags["TagList"]], action, selector
                    )

                    resource_details = {
                        "resourceArn": instance["DBInstanceArn"],
                        "details": {"instanceIdentifier": instance["DBInstanceIdentifier"]},
                        "nextEventTime": instance_event_time,
                    }

                    if instance_event_time:
                        print(
                            f">> RDS instance {instance['DBInstanceIdentifier']} will {action} on {instance_event_time}"
                        )

                        payload.append(resource_details)
                    else:
                        print(
                            f">> No {action} event for RDS instance {instance['DBInstanceIdentifier']} in the next 24 hours"
                        )

                params["Marker"] = describe_response.get("Marker", "")
            else:
                break

        return payload
