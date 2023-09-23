import os
from datetime import datetime

import boto3
from tools import get_event_timestamp


class ECS:
    def __init__(self):
        self.ecs_client = boto3.client("ecs")

    def list_resources(self, action: str, selector: str):
        """
        Get all ECS services in the account and return them as a list

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

        print(">> Listing ECS services")

        while params.get("nextToken") != "":
            list_response = self.ecs_client.list_clusters(**params)

            if len(list_response["clusterArns"]) != 0:
                desribe_response = self.ecs_client.describe_clusters(
                    clusters=list_response["clusterArns"], include=["TAGS"]
                )

                for cluster in desribe_response["clusters"]:
                    cluster_event_time = get_event_timestamp(cluster["tags"], action, selector)

                    services = self.get_ecs_services(
                        cluster_arn=cluster["clusterArn"],
                        action=action,
                        selector=selector,
                        cluster_event_time=cluster_event_time,
                    )

                    for service in services:
                        payload.append(service)

                params["nextToken"] = list_response.get("nextToken", "")
            else:
                break

        payload = sorted(payload, key=lambda x: x["nextEventTime"])

        return payload

    def get_ecs_services(self, cluster_arn: str, action: str, selector: str, cluster_event_time: str):
        """
        Get all ECS services in the cluster

        Parameters
        ----------
        cluster_arn : str
            The cluster arn
        action : str
            The action of the event (start or stop)
        selector : str
            The tags selector in case of manual action
        cluster_event_time : str
            The next event time for the cluster

        Returns
        -------
        services : List[Service]
        """
        services = []
        params = {}

        while params.get("nextToken") != "":
            list_response = self.ecs_client.list_services(cluster=cluster_arn, **params)

            if len(list_response["serviceArns"]) != 0:
                describe_response = self.ecs_client.describe_services(
                    cluster=cluster_arn,
                    services=list_response["serviceArns"],
                    include=["TAGS"],
                )

                for service in describe_response["services"]:
                    service_event_time = get_event_timestamp(service["tags"], action, selector)

                    if service_event_time and not cluster_event_time:
                        resource_event_time = service_event_time
                    elif service_event_time and cluster_event_time:
                        resource_event_time = service_event_time
                    elif not service_event_time and cluster_event_time:
                        resource_event_time = cluster_event_time
                    else:
                        print(
                            f">> No {action} event for service {service['serviceName']} in the next {os.environ.get('EXECUTION_INTERVAL')} hours"
                        )
                        continue

                    services.append(
                        {
                            "resourceArn": service["serviceArn"],
                            "details": {
                                "serviceName": service["serviceName"],
                                "clusterName": service["clusterArn"].split("/")[-1],
                            },
                            "resourceTtl": str(int(datetime.now().timestamp()) + 60 * 60 * 24 * 30),
                            "nextEventTime": resource_event_time,
                        }
                    )

                    print(f">> ECS Service {service['serviceName']} will {action} on {resource_event_time}")

                params["nextToken"] = list_response.get("nextToken", "")
            else:
                break

        return services
