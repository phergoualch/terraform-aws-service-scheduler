import pytest
from services import EC2
from models.enums import Action
from models import Resource, Tag


@pytest.fixture
def service():
    action = Action.START
    parameters = {
        "tags_prefix": "scheduler",
        "tags_mapping": {
            tag: tag
            for tag in [
                "enabled",
                "time",
                "timezone",
                "active-days",
                "active-days-of-month",
                "active-weeks",
                "active-months",
                "parameter",
            ]
        },
        "default_timezone": "UTC",
        "interval": "6",
        "schedule_without_tags": True,
        "default_schedule": {
            "start-time": "08:00",
            "stop-time": "18:00",
            "active-days": "MON-FRI",
        },
    }
    service = EC2(action, parameters)
    return service


@pytest.fixture
def resource(service):
    resource = Resource(id_="arn", service=service, tags=set([]))
    return resource


@pytest.fixture
def resource_overwrite(service):
    resource = Resource(
        id_="arn", service=service, tags=set([Tag("scheduler:start-time", "10:00")])
    )
    return resource


def test_schedule(resource):
    schedule = resource.get_schedule_from_tags()
    assert schedule.time == "08:00"
    assert schedule.active_days == "MON-FRI"


def test_schedule_overwrite(resource_overwrite):
    schedule = resource_overwrite.get_schedule_from_tags()
    assert schedule.time == "10:00"
    assert schedule.active_days == "MON-FRI"
