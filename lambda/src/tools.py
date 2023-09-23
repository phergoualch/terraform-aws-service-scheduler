import os
from datetime import datetime, timedelta

from dateutil import tz


def get_event_timestamp(tags, action, selector):
    """
    Get the event timestamp from the tags

    Parameters
    ----------
    tags : List[dict]
        The tags for the resource
    action : str
        The action of the event (start or stop)
    selector : str
        The tags selector in case of manual action

    Returns
    -------
    event_timestamp : str
        The event timestamp in the ISO 8601 format
    """

    if len(selector) > 0:
        now = datetime.now(tz.gettz(os.environ.get("DEFAULT_TIMEZONE"))).isoformat()
        if selector == "all":
            return now
        elif check_manual_trigger(tags, selector):
            return now
        else:
            return None

    else:
        resource_values = get_resource_values(tags, action)

        if not resource_values:
            return None

        next_event = get_next_event_datetime(resource_values)

        if is_next_event_within_x_hours(next_event, int(os.environ.get("EXECUTION_INTERVAL"))):
            return next_event.isoformat()

    return None


def get_resource_values(tags, action):
    """
    Get the resource values from the tags

    Parameters
    ----------
    tags : List[dict]
        The tags for the resource
    action : str
        The action of the event (start or stop)

    Returns
    -------
    resource_values : dict
    """
    resource_values = {
        "event_time": None,
        "active_days": None,
        "event_timezone": os.environ.get("DEFAULT_TIMEZONE"),
    }

    for tag in tags:
        if tag["key"] == f"finops:{action}-time":
            resource_values["event_time"] = tag["value"]
        elif tag["key"] == "finops:active-days":
            resource_values["active_days"] = tag["value"]
        elif tag["key"] == f"finops:{action}-active-days":
            resource_values["active_days"] = tag["value"]
        elif tag["key"] == f"finops:timezone":
            resource_values["event_timezone"] = tag["value"]
        elif tag["key"] == f"finops:enabled" and tag["value"] != "true":
            return None

    if not resource_values["event_time"] or not resource_values["active_days"]:
        return None
    else:
        return resource_values


def check_manual_trigger(tags, selector):
    print(">> Checking manual trigger")
    print(f">> Selector: {selector}")
    key_value_pairs = selector.split(",")

    selector_dict = {key: [] for key, _ in [pair.split("=") for pair in key_value_pairs]}

    for pair in key_value_pairs:
        key, value = pair.split("=")
        selector_dict[key].append(value)

    print(f">> Selector dict: {selector_dict}")

    selector_check = {key: False for key in selector_dict}
    finops_enabled = False

    for tag in tags:
        for key in selector_dict:
            if tag["key"] == key and tag["value"] in selector_dict[key]:
                selector_check[key] = True
            elif tag["key"] == f"finops:enabled" and tag["value"] == "true":
                finops_enabled = True

    if all(selector_check.values()) and finops_enabled:
        return True


def is_day_in_range(day, day_range):
    """
    Check if a given day is in a given day range

    Parameters
    ----------
    day : str
        The day to check
    day_range : str
        The day range to check against
        Format: MON-SUN or MON,TUE,WED or MON,TUE-FRI,SUN or MON

    Returns
    -------
    bool
    """
    day_range = day_range.upper()

    # Split the day_range string into individual day parts
    day_parts = day_range.split(",")

    # Define a dictionary to map day abbreviations to their respective numeric values
    day_mapping = {"MON": 0, "TUE": 1, "WED": 2, "THU": 3, "FRI": 4, "SAT": 5, "SUN": 6}

    for part in day_parts:
        if "-" in part:
            start_day, end_day = part.split("-")
            start_val = day_mapping[start_day]
            end_val = day_mapping[end_day]

            if start_val <= end_val:
                if start_val <= day_mapping[day] <= end_val:
                    return True
            else:
                if start_val <= day_mapping[day] or day_mapping[day] <= end_val:
                    return True
        else:
            if "," in part:
                sub_parts = part.split("-")
                for sub_part in sub_parts:
                    if day_mapping[day] == day_mapping[sub_part]:
                        return True
            else:
                if day_mapping[day] == day_mapping[part]:
                    return True

    return False


def get_next_event_datetime(resource_values):
    """
    Get the next occurrence of the event in a datetime format

    Parameters
    ----------
    resource_values : dict
        Dictionary containing the event information including:
        - "event_time": The time of the event in the format 'HH:mm'
        - "event_range": The day range of the event in the format 'MON-SUN'
        - "event_timezone": The timezone of the event in the format 'America/New_York'

    Returns
    -------
    next_event_datetime : datetime
        The next occurrence of the event as a datetime object
    """
    # Parse the event_time to create a time object
    event_time = datetime.strptime(resource_values["event_time"], "%H:%M").time()

    # Get the current date in the event_timezone
    current_datetime = datetime.now(tz.gettz(resource_values["event_timezone"]))

    # Initialize the next event datetime as None
    next_event_datetime = None

    # Check if the event is today and has not passed yet
    if (
        is_day_in_range(current_datetime.strftime("%a").upper(), resource_values["active_days"])
        and current_datetime.time() < event_time
    ):
        next_event_datetime = current_datetime.replace(
            hour=event_time.hour, minute=event_time.minute, second=0, microsecond=0
        )
    else:
        # Find the next occurrence of the event
        next_day = current_datetime + timedelta(days=1)
        while not is_day_in_range(next_day.strftime("%a").upper(), resource_values["active_days"]):
            next_day += timedelta(days=1)

        return next_day.replace(hour=event_time.hour, minute=event_time.minute, second=0, microsecond=0)

    return next_event_datetime


def is_next_event_within_x_hours(next_event, period):
    """
    Check if the next event is happening in the next X hours based on the current UTC time

    Parameters
    ----------
    next_event : datetime
        The next event datetime to check
    period : int
        Number of hours to check if the event is happening within

    Returns
    -------
    bool
        True if the next event is happening within the next X hours, False otherwise
    """
    # Get the current UTC time
    current_utc = datetime.now(tz.UTC)

    # Convert the next event datetime to UTC
    next_event_utc = next_event.astimezone(tz.UTC)

    # Check if the next event is happening within the next X hours
    return next_event_utc - current_utc <= timedelta(hours=period)
