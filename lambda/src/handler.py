from services import ASG, EC2, ECS, RDS, DocumentDB, Lambda, AppRunner


def handler(event, context):
    service = event["service"]
    action = event["details"]["action"]
    selector = event["details"].get("selector", "")
    services = event["details"].get("services", None)
    if not services or services == "all" or service in services.split(","):
        pass
    else:
        return []

    if service == "ecs":
        return ECS().list_resources(action=action, selector=selector)

    elif service == "asg":
        return ASG().list_resources(action=action, selector=selector)

    elif service == "documentdb":
        return DocumentDB().list_resources(action=action, selector=selector)

    elif service == "rds":
        return RDS().list_resources(action=action, selector=selector)

    elif service == "lambda":
        return Lambda().list_resources(action=action, selector=selector)

    elif service == "ec2":
        return EC2().list_resources(action=action, selector=selector)

    elif service == "apprunner":
        return AppRunner().list_resources(action=action, selector=selector)

    else:
        raise Exception(f"Service {service} is not supported")
