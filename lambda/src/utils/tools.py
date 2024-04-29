from enum import Enum
import logging
from typing import Set

from models.tag import Tag

logger = logging.getLogger(__name__)


def is_in_range(value: str, range_value: str, range_enum: Enum = None):
    """
    Check if a given value is in a given range.

    Parameters
    ----------
    value : int or str
        The value to check.
    range_value : str
        The range to check against.
        Format: MON-SUN or 1,12,31 or JAN,MAR-AUG,DEC or 3.
    range_enum : Enum, optional
        An Enum mapping values to their corresponding Enum values, e.g., Day, Month, by default None.

    Returns
    -------
    bool
        True if the value is in the specified range, False otherwise.
    """
    if str(value) == "0":
        return False

    parts = range_value.replace(" ", "").split(",")

    for part in parts:
        target = value
        if "-" in part:
            start, end = part.split("-")
            if range_enum:
                start = range_enum[start].value
                end = range_enum[end].value
                target = range_enum[target].value
            if int(start) <= int(end):
                if int(start) <= int(target) <= int(end):
                    return True
            else:
                if int(start) <= int(target) or int(target) <= int(end):
                    return True
        else:
            if range_enum:
                part = range_enum[part].value
                target = range_enum[target].value
            if int(target) == int(part):
                return True

    return False


def check_selector_tags(tags: Set[Tag], selector: str) -> bool:
    """
    Check if the selector tags are present in the resource tags.

    Parameters
    ----------
    tags : Set[Tag]
        List of Tag objects containing key-value pairs.
    selector : str
        Selector string in the format "key1=value1,key2=value2,...".

    Returns
    -------
    bool
        True if all conditions are met, False otherwise.
    """
    if selector == "all":
        return True

    try:
        selectors_dict = {}
        for pair in selector.split(","):
            key, value = pair.split("=")

            if key in selectors_dict:
                selectors_dict[key].append(value)
            else:
                selectors_dict[key] = [value]

        selectors_check = []

        for key, values in selectors_dict.items():
            for tag in tags:
                if tag.key == key and tag.value in values:
                    selectors_check.append(True)
                    break
            else:
                selectors_check.append(False)

        return all(selectors_check)

    except Exception as e:
        logger.error(f"Error checking selector tags: {e}")
        return False
