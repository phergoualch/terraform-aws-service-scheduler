from handler import handler
import pytest
import os
import datetime
from dateutil import tz


def set_env_vars():
    os.environ["DEFAULT_TIMEZONE"] = "Europe/Paris"
    os.environ["EXECUTION_INTERVAL"] = "24"
    os.environ["TAGS_PREFIX"] = "scheduler"
    os.environ["TAGS_MAPPING"] = (
        '{"active-days":"active-days","active-days-of-month":"active-days-of-month","active-months":"active-months","active-weeks":"active-weeks","enabled":"enabled","parameter":"parameter","time":"time","timezone":"timezone"}'
    )


def test_handler_auto():
    set_env_vars()
    event = {
        "service": "ec2",
        "action": "stop",
        "input": {},
    }
    response = handler(event, None)
    assert all([all([key in item for key in ["attributes", "id", "nextExecutionTime"]]) for item in response])


@pytest.mark.parametrize("service", ["ec2", "documentdb", "asg", "apprunner", "rds", "aurora", "ecs", "lambda"])
def test_handler_manual(service):
    set_env_vars()
    event = {
        "service": service,
        "action": "stop",
        "input": {
            "selectors": [
                {
                    "tags": "all",
                    "services": "ec2",
                    "delay": 0,
                }
            ]
        },
    }
    response = handler(event, None)
    assert all([all([key in item for key in ["attributes", "id", "nextExecutionTime"]]) for item in response])
    times_check = []
    for item in response:
        time = datetime.datetime.now(tz=tz.gettz("Europe/Paris")).replace(second=0, microsecond=0)
        times_check.append(time <= datetime.datetime.fromisoformat(item["nextExecutionTime"]) <= time + datetime.timedelta(minutes=1))
    assert all(times_check)


@pytest.mark.parametrize("service", ["ec2", "documentdb", "asg", "apprunner", "rds", "aurora", "ecs", "lambda"])
def test_handler_auto(service):
    set_env_vars()
    event = {
        "service": service,
        "action": "stop",
        "input": {},
    }
    response = handler(event, None)
    assert all(
        [
            item["nextExecutionTime"]
            == datetime.datetime.now(tz=tz.gettz("Europe/Paris")).replace(hour=18, minute=0, second=0, microsecond=0).isoformat()
            for item in response
        ]
    )
