# ruff: noqa: F811
from datetime import datetime

import pytest
from dateutil import tz
from models import Resource, Tag
from models.enums import Day, Month, Action
from utils.tools import is_in_range

from tests.test_global import service  # noqa: F401


@pytest.fixture
def resource(service):
    resource = Resource(
        id_="arn",
        service=service,
        tags=set(
            [
                Tag("scheduler:enabled", "true"),
                Tag("scheduler:start-time", "10:00"),
                Tag("scheduler:timezone", "UTC"),
                Tag("app", "test"),
            ]
        ),
        attributes={"id": "id"},
    )
    return resource


def test_schedule(resource):
    schedule = resource.get_schedule_from_tags()
    assert schedule.time == "10:00"
    assert schedule.timezone == "UTC"


def test_is_day_in_range():
    assert is_in_range(Day.MON.name, "MON-SUN", range_enum=Day)
    assert is_in_range(Day.TUE.name, "SAT-WED", range_enum=Day)
    assert not is_in_range(Day.TUE.name, "FRI-SUN", range_enum=Day)


def test_is_month_in_range():
    assert is_in_range(Month.MAR.name, "JAN-APR", range_enum=Month)
    assert is_in_range(Month.JUL.name, "JUL,DEC", range_enum=Month)
    assert not is_in_range(Month.AUG.name, "JAN,APR-JUL,OCT", range_enum=Month)


def test_is_number_in_range():
    assert is_in_range(17, "10-31")
    assert is_in_range(3, "1,3,7")
    assert not is_in_range(0, "1-31")
    assert not is_in_range(32, "1-31")
    assert not is_in_range(17, "1-16,18-31")
    assert is_in_range(23, "17-28,19-37")


def test_get_next_execution_time(resource):
    resource.service.now = datetime(2024, 1, 26, 8, 0, 0, tzinfo=tz.gettz("UTC"))
    schedule = resource.get_schedule_from_tags()
    assert schedule.get_next_execution_time() == datetime(
        2024, 1, 26, 10, 0, 0, tzinfo=tz.gettz("UTC")
    )
    resource.service.now = datetime(2024, 1, 26, 14, 0, 0, tzinfo=tz.gettz("UTC"))
    schedule = resource.get_schedule_from_tags()
    assert schedule.get_next_execution_time() is None


def test_get_next_execution_time_next_day(service):
    resource = Resource(
        id_="arn",
        service=service,
        tags=set(
            [
                Tag("scheduler:enabled", "true"),
                Tag("scheduler:start-time", "03:00"),
                Tag("scheduler:timezone", "UTC"),
                Tag("scheduler:active-days", "WED-FRI, SAT"),
            ]
        ),
    )
    resource.service.now = datetime(2024, 1, 26, 22, 0, 0, tzinfo=tz.gettz("UTC"))
    schedule = resource.get_schedule_from_tags()
    assert schedule.get_next_execution_time() == datetime(
        2024, 1, 27, 3, 0, 0, tzinfo=tz.gettz("UTC")
    )
    resource.service.now = datetime(2024, 1, 26, 18, 0, 0, tzinfo=tz.gettz("UTC"))
    schedule = resource.get_schedule_from_tags()
    assert schedule.get_next_execution_time() is None


def test_schedules_iterators(service):
    resource = Resource(
        id_="arn",
        service=service,
        tags=(
            [
                Tag("scheduler:enabled", "true"),
                Tag("scheduler:start-time", "09:00"),
                Tag("scheduler:active-days", "MON-FRI"),
                Tag("scheduler:active-months", "JAN-DEC"),
                Tag("scheduler:start-time:1", "13:00"),
                Tag("scheduler:active-days:1", "SAT-SUN"),
            ]
        ),
    )
    schedules = []
    for iterator in resource.iterators:
        schedule = resource.get_schedule_from_tags(iterator=iterator.iterator)
        schedules.append(schedule)

    assert len(schedules) == 2
    assert schedules[0].active_days == "MON-FRI"
    assert schedules[0].active_months == "JAN-DEC"
    assert schedules[1].active_months == "JAN-DEC"


def test_multi_schedule_same_day(service):
    service.action = Action.STOP
    resource = Resource(
        id_="arn",
        service=service,
        tags=(
            [
                Tag("scheduler:enabled", "true"),
                Tag("scheduler:start-time", "08:00"),
                Tag("scheduler:stop-time", "18:00"),
                Tag("scheduler:start-time:1", "23:00"),
                Tag("scheduler:stop-time:1", "02:00"),
                Tag("scheduler:start-active-days-of-month:1", "1"),
                Tag("scheduler:stop-active-days-of-month:1", "2"),
            ]
        ),
    )

    resource.service.now = datetime(2024, 1, 1, 14, 0, 0, tzinfo=tz.gettz("UTC"))
    resource.get_next_execution_time_auto()

    assert resource.next_execution_time == datetime(
        2024, 1, 1, 18, 0, 0, tzinfo=tz.gettz("UTC")
    )

    resource = Resource(
        id_="arn",
        service=service,
        tags=(
            [
                Tag("scheduler:enabled", "true"),
                Tag("scheduler:start-time", "08:00"),
                Tag("scheduler:stop-time", "18:00"),
                Tag("scheduler:start-time:1", "23:00"),
                Tag("scheduler:stop-time:1", "02:00"),
                Tag("scheduler:start-active-days-of-month:1", "1"),
                Tag("scheduler:stop-active-days-of-month:1", "2"),
            ]
        ),
    )

    resource.service.now = datetime(2024, 1, 1, 22, 0, 0, tzinfo=tz.gettz("UTC"))
    resource.get_next_execution_time_auto()

    assert resource.next_execution_time == datetime(
        2024, 1, 2, 2, 0, 0, tzinfo=tz.gettz("UTC")
    )


def test_ignore_empty_time(service):
    resource = Resource(
        id_="arn",
        service=service,
        tags=set(
            [
                Tag("scheduler:start-time", ""),
                Tag("scheduler:timezone", "UTC"),
                Tag("scheduler:active-days", "WED-FRI, SAT"),
            ]
        ),
    )
    resource.service.now = datetime(2024, 1, 26, 22, 0, 0, tzinfo=tz.gettz("UTC"))
    schedule = resource.get_schedule_from_tags()

    assert schedule.get_next_execution_time() is None
