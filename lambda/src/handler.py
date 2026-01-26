import logging

from models import Service
from models.enums import Action
from services import (
    ASG,
    EC2,
    ECS,
    RDS,
    AppRunner,
    Aurora,
    Cloudwatch,
    DocumentDB,
    Elasticache,
    Lambda,
)

logger = logging.getLogger("handler")


def ServiceFactory(service: str, action: Action) -> Service:
    """
    Create and return an instance of the specified service based on the provided service name and action.

    Parameters
    ----------
    service : str
        The name of the service.
    action : Action
        The action to be performed (start or stop).

    Returns
    -------
    Service
        An instance of the specified service.
    """
    services = {
        "ec2": EC2,
        "documentdb": DocumentDB,
        "asg": ASG,
        "apprunner": AppRunner,
        "rds": RDS,
        "aurora": Aurora,
        "ecs": ECS,
        "lambda": Lambda,
        "elasticache": Elasticache,
        "cloudwatch": Cloudwatch,
    }

    return services[service](action)


def handler(event, context):
    """
    Lambda handler function to process resources based on the specified service and action.

    Parameters
    ----------
    event : dict
        The Lambda event object.
    context : LambdaContext
        The Lambda context object.

    Returns
    -------
    List[dict]
        A list of JSON representations of resources with their next execution times.
    """
    service_name = event["service"]
    selectors = event["input"].get("selectors", None)
    payload = []

    service = ServiceFactory(service_name, Action(event["action"]))

    logger.info(f"Processing {service.action.value} for {service_name} resources")

    resources = service.list_resources()

    for resource in resources:
        try:
            if resource.enabled:
                if selectors:
                    resource.get_next_execution_time_manual(selectors=selectors)
                else:
                    resource.get_next_execution_time_auto()

                if resource.next_execution_time:
                    logger.info(
                        f"Next {service.action.value} time for {resource.id} is {resource.next_execution_time}"
                    )
                    payload.append(resource)
                else:
                    logger.info(f"No {service.action.value} time for {resource.id}")
        except Exception as e:
            logger.error(f"Error processing resource {resource.id}: {e!s}")

    return [
        resource.to_json()
        for resource in sorted(payload)
        if resource.next_execution_time
    ]
