from datetime import datetime, timedelta
from dateutil import tz

from models.enums import Day, Month
from models.resource import Resource
from utils.tools import is_in_range


class Schedule:
    """
    Represents a schedule.

    Attributes
    ----------
    resource : Resource
        The associated resource.
    time : str
        The scheduled time.
    timezone : str
        The timezone.
    active_days : str
        The active days.
    active_days_of_month : str
        The active days of the month.
    active_weeks : str
        The active weeks.
    active_months : str
        The active months.

    Methods
    -------
    __repr__()
        Return a string representation of the schedule.
    get_next_execution_time()
        Get the next execution time.

    Examples
    --------
    Creating a Schedule instance:

    >>> schedule = Schedule(resource=my_resource, time="08:00", timezone="UTC", active_days="MON-FRI", active_days_of_month="1-31", active_weeks="1-53", active_months="JAN-DEC")

    Getting the next execution time:

    >>> schedule.get_next_execution_time()
    datetime.datetime(...)

    """

    def __init__(
        self,
        resource: Resource,
        time: str,
        timezone: str,
        active_days: str,
        active_days_of_month: str,
        active_weeks: str,
        active_months: str,
    ):
        """
        Initialize a Schedule instance.

        Parameters
        ----------
        resource : Resource
            The associated resource.
        time : str
            The scheduled time.
        timezone : str
            The timezone.
        active_days : str
            The active days.
        active_days_of_month : str
            The active days of the month.
        active_weeks : str
            The active weeks.
        active_months : str
            The active months.
        """
        self.resource = resource

        self.time = time
        self.timezone = timezone

        self.active_days = active_days
        self.active_days_of_month = active_days_of_month
        self.active_weeks = active_weeks
        self.active_months = active_months

    def __repr__(self):
        """
        Return a string representation of the schedule.

        Returns
        -------
        str
            A string representation of the schedule.
        """
        return f"Schedule(time={self.time}, timezone={self.timezone}, active_days={self.active_days}, active_days_of_month={self.active_days_of_month}, active_weeks={self.active_weeks}, active_months={self.active_months})"

    def get_next_execution_time(self) -> datetime:
        """
        Get the next execution time for the schedule if it's in the interval.

        Returns
        -------
        datetime
            The next execution time if it's in the interval, None otherwise.
        """
        current_time = self.resource.service.now.astimezone(tz.gettz(self.timezone))
        interval_time = (self.resource.service.now + timedelta(hours=self.resource.service.interval)).astimezone(tz.gettz(self.timezone))

        scheduled_time = datetime.strptime(self.time, "%H:%M").replace(
            year=current_time.year,
            month=current_time.month,
            day=current_time.day,
            tzinfo=tz.gettz(self.timezone),
        )

        if current_time <= scheduled_time <= interval_time or scheduled_time + timedelta(days=1) <= interval_time:
            if is_in_range(current_time.strftime("%a").upper(), self.active_days, range_enum=Day):
                if is_in_range(current_time.day, self.active_days_of_month):
                    if is_in_range(current_time.strftime("%U"), self.active_weeks):
                        if is_in_range(
                            current_time.strftime("%b").upper(),
                            self.active_months,
                            range_enum=Month,
                        ):
                            return scheduled_time if current_time <= scheduled_time <= interval_time else scheduled_time + timedelta(days=1)

        return None
