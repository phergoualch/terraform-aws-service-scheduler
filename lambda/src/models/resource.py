from typing import Dict, List
from datetime import timedelta
from dateutil import tz
import json
import logging

from models.service import Service
from models.tag import Tag
from models.iterator import Iterator, IteratorType
from utils.tools import check_selector_tags

logger = logging.getLogger(__name__)


class Resource:
    """
    Represents a resource.

    Attributes
    ----------
    id : str
        The ID of the resource.
    service : Service
        The associated service.
    tags : List[Tag]
        The list of tags associated with the resource.
    attributes : Dict
        Additional attributes.
    enabled : bool
        True if the resource is enabled (has the enabled tag set to true).
    iterators: List[Dict]
        The list of iterators associated with the resource and if they are of type parameter or tag.
    next_execution_time : datetime
        The next scheduled execution time of the resource.

    Methods
    -------
    __eq__(other)
        Compare the resource with another resource for equality.
    __lt__(other)
        Compare the resource with another resource for less than.
    __repr__()
        Return a string representation of the resource.
    get_schedule_attributes()
        Get the resource scheduler attributes from the resource tags.
    get_schedule_from_tags(iterator)
        Get the resource scheduler values from the resource tags.
    load_tags_from_parameter(iterator)
        Load the resource tags from the parameter store parameter.
    get_next_execution_time_auto()
        Calculate and set the next scheduled execution time automatically based on resource tags.
    get_next_execution_time_manual(selectors)
        Calculate and set the next scheduled execution time manually based on selector conditions.
    to_json()
        Return a JSON representation of the resource to return to Step Functions.
    """

    def __init__(self, id_: str, service: Service, tags: List[Tag], attributes: Dict = None):
        """
        Initialize a Resource instance.

        Parameters
        ----------
        id_ : str
            The ID of the resource.
        service : Service
            The associated service.
        tags : List[Tag]
            The list of tags associated with the resource.
        attributes : Dict, optional
            Additional attributes, by default None.
        """
        self.id = id_
        self.service = service
        self.tags = tags
        self.attributes = attributes

        self.enabled = False
        self.iterators = []
        self.next_execution_time = None

        self.get_schedule_attributes()

        # Load tags from parameters to the resource
        if any(iterator.type == IteratorType.PARAMETER for iterator in self.iterators) and self.enabled:
            for iterator in self.iterators:
                if iterator.type == IteratorType.PARAMETER:
                    self.load_tags_from_parameter(iterator=iterator.iterator)

        # Disable the the resource if it does not have a time tag
        if not any(tag.key == self.service.get_tag_key("time", action=True) for tag in self.tags):
            self.enabled = False

    def __eq__(self, other):
        """
        Compare the resource with another resource for equality.

        Parameters
        ----------
        other : Resource
            The resource to compare with.

        Returns
        -------
        bool
            True if the resources are equal, False otherwise.
        """
        return self.id == other.id

    def __lt__(self, other):
        """
        Compare the resource with another resource for less than.

        Parameters
        ----------
        other : Resource
            The resource to compare with.

        Returns
        -------
        bool
            True if the resource is less than the other resource, False otherwise.
        """
        return self.next_execution_time < other.next_execution_time

    def __repr__(self):
        """
        Return a string representation of the resource.

        Returns
        -------
        str
            A string representation of the resource.
        """
        return f"Resource(id={self.id}, attributes={self.attributes})"

    def get_schedule_attributes(self):
        """
        Get the resource scheduler attributes from the resource tags.

        Returns
        -------
        enabled : bool
            True if the resource is enabled.
        """

        iterators = set()

        for tag in self.tags:
            if tag.key == self.service.get_tag_key("enabled"):
                if tag.value == "true":
                    self.enabled = True

            split = tag.key.split(":")
            if split[-1].isdigit():
                iterator = int(split[-1])
                if self.service.get_tag_key("parameter", iterator=iterator) == tag.key:
                    iterators.add(Iterator(iterator=iterator, type=IteratorType.PARAMETER))
                else:
                    iterators.add(Iterator(iterator=iterator, type=IteratorType.TAG))
            else:
                iterators.add(
                    Iterator(iterator=None, type=IteratorType.PARAMETER)
                    if self.service.get_tag_key("parameter") == tag.key
                    else Iterator(iterator=None, type=IteratorType.TAG)
                )

        self.iterators = sorted(list(iterators))

    def get_schedule_from_tags(self, iterator: int = None):
        """
        Get the resource scheduler values from the resource tags.

        Parameters
        ----------
        iterator : int, optional
            The iterator to use, by default None.
        Returns
        -------
        schedule: Schedule
            The schedule object built from the resource tags.
        """
        from models.schedule import Schedule

        schedule_attributes = {
            "time": None,
            "timezone": self.service.default_timezone,
            "active_days": "MON-SUN",
            "active_days_of_month": "1-31",
            "active_weeks": "1-53",
            "active_months": "JAN-DEC",
        }

        tag_patterns = [
            {"key": "time", "action": True},
            {"key": "time", "action": True, "iterator": iterator},
            {"key": "timezone"},
            {"key": "timezone", "iterator": iterator},
            {"key": "active-days"},
            {"key": "active-days", "action": True},
            {"key": "active-days", "iterator": iterator},
            {"key": "active-days", "action": True, "iterator": iterator},
            {"key": "active-days-of-month"},
            {"key": "active-days-of-month", "iterator": iterator},
            {"key": "active-days-of-month", "action": True},
            {"key": "active-days-of-month", "action": True, "iterator": iterator},
            {"key": "active-weeks"},
            {"key": "active-weeks", "iterator": iterator},
            {"key": "active-weeks", "action": True},
            {"key": "active-weeks", "action": True, "iterator": iterator},
            {"key": "active-months"},
            {"key": "active-months", "iterator": iterator},
            {"key": "active-months", "action": True},
            {"key": "active-months", "action": True, "iterator": iterator},
        ]

        for pattern in tag_patterns:
            tag_key = self.service.get_tag_key(pattern["key"], action=pattern.get("action", False), iterator=pattern.get("iterator", None))
            matching_tag = next((tag for tag in self.tags if tag.key == tag_key), None)
            if matching_tag:
                schedule_attributes[pattern["key"].replace("-", "_")] = matching_tag.value

        return Schedule(resource=self, **schedule_attributes)

    def load_tags_from_parameter(self, iterator: int = None):
        """
                Load the resource tags from the parameter store parameter.

                Parameters
                ----------
                iterator : int, optional
                    The iterator to use, by default None

        .
        """
        parameter_tag = self.service.get_tag_key("parameter", iterator=iterator)
        parameter_name = next((tag.value for tag in self.tags if tag.key == parameter_tag), None)

        try:
            tags = self.service.ssm.get_parameter(Name=parameter_name)["Parameter"]["Value"]
        except Exception as e:
            logger.warning(f"Could not load tags from parameter {parameter_tag}: {e}")
            return

        parameter_tags = []

        for key, value in json.loads(tags).items():
            try:
                parameter_tags.append(
                    Tag(
                        key=f"{self.service.tags_prefix}:{key}:{iterator}" if iterator else f"{self.service.tags_prefix}:{key}", value=value
                    )
                )
            except Exception as e:
                logger.warning(f"Could not load tag {key} from parameter {parameter_tag}: {e}")
                continue

        self.tags.extend(parameter_tags)

    def get_next_execution_time_auto(self):
        """
        Calculate and set the next scheduled execution time automatically based on resource tags.
        """
        for iterator in self.iterators:
            schedule = self.get_schedule_from_tags(iterator=iterator.iterator)
            next_execution_time = schedule.get_next_execution_time()
            if next_execution_time:
                self.next_execution_time = next_execution_time

    def get_next_execution_time_manual(self, selectors: List[Dict]):
        """
        Calculate and set the next scheduled execution time manually based on selector conditions.

        Parameters
        ----------
        selectors : List[Dict]
            List of selector conditions.
        """
        for selector in selectors:
            if self.service.name in selector["services"].split(",") or selector["services"] == "all":
                if check_selector_tags(self.tags, selector["tags"]):
                    self.next_execution_time = self.service.now + timedelta(minutes=selector.get("delay", 0))
                    # Get current timezone and set the next execution time to the next minute to avoid running the resource immediately
                    self.next_execution_time = self.next_execution_time.replace(tzinfo=tz.tzlocal()).replace(microsecond=0)
                    break
        else:
            self.next_execution_time = None

    def to_json(self):
        """
        Return a JSON representation of the resource to return to Step Functions.

        Returns
        -------
        dict
            The JSON representation of the resource.
        """

        return {
            "id": self.id,
            "attributes": self.attributes,
            "nextExecutionTime": self.next_execution_time.isoformat() if self.next_execution_time else None,
            "ttl": str(int((self.next_execution_time + timedelta(days=365)).timestamp())) if self.next_execution_time else None,
        }
