import pytest
from services import EC2
from models import Resource, Tag
from models.enums import Action
from utils.tools import check_selector_tags
from datetime import timedelta
from dateutil import tz


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
    }
    service = EC2(action, parameters)
    return service


@pytest.fixture
def resource(service):
    resource = Resource(
        "arn",
        service,
        [
            Tag("scheduler:enabled", "true"),
            Tag("scheduler:start-time", "10:00"),
            Tag("scheduler:timezone", "UTC"),
        ],
        {"id": "id"},
    )
    return resource


def test_tag():
    tag = Tag("key", "value")
    assert tag.key == "key"
    assert tag.value == "value"


def test_service(service):
    assert service.name == "ec2"
    assert service.action == Action.START
    assert service.tags_prefix == "scheduler"
    assert service.default_timezone == "UTC"
    assert service.interval == 6
    assert service.tags_mapping == {
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
    }


def test_resource(resource):
    assert resource.id == "arn"
    assert all([isinstance(tag, Tag) for tag in resource.tags])
    assert resource.attributes == {"id": "id"}


def test_resource_is_enabled(resource):
    assert resource.enabled == True


def test_resource_is_enabled_missing_tag(service):
    resource = Resource("arn", service, [Tag("scheduler:wrong_tag", "true")])
    assert resource.enabled == False


def test_get_tag_key(service):
    assert service.get_tag_key("enabled") == "scheduler:enabled"
    assert service.get_tag_key("time", action=True) == "scheduler:start-time"
    assert (
        service.get_tag_key("active-months", action=True, iterator=3)
        == "scheduler:start-active-months:3"
    )
    assert service.get_tag_key("active-days", iterator=1) == "scheduler:active-days:1"


@pytest.fixture
def resource1(service):
    resource = Resource(
        "arn",
        service,
        [
            Tag("scheduler:enabled", "true"),
            Tag("application", "app1"),
            Tag("environment", "dev"),
            Tag("team", "team1"),
        ],
    )
    return resource


@pytest.mark.parametrize("delay", [0, 5, 10])
def test_manual_delay(delay, resource):
    selectors = [{"services": "ec2", "tags": "all", "delay": delay}]
    resource.get_next_execution_time_manual(selectors=selectors)

    assert resource.next_execution_time == (
        resource.service.now + timedelta(minutes=delay)
    ).replace(microsecond=0, tzinfo=tz.tzlocal())


@pytest.fixture
def resource2(service):
    resource = Resource(
        "arn",
        service,
        [
            Tag("scheduler:enabled", "true"),
            Tag("application", "app2"),
            Tag("environment", "prod"),
            Tag("team", "team1"),
        ],
    )
    return resource


@pytest.mark.parametrize(
    "selector, expected",
    [
        ("all", [True, True]),
        ("any", [False, False]),
        ("application=app1", [True, False]),
        ("application=app1,application=app2", [True, True]),
        ("team=team1", [True, True]),
    ],
)
def test_check_selector_tags(selector, expected, resource1, resource2):
    assert check_selector_tags(resource1.tags, selector) == expected[0]
    assert check_selector_tags(resource2.tags, selector) == expected[1]
