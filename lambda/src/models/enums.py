import enum


class Action(enum.Enum):
    """
    Represents possible actions.

    Attributes
    ----------
    START : str
        Start action.
    STOP : str
        Stop action.
    """

    START = "start"
    STOP = "stop"


class Day(enum.Enum):
    """
    Represents days of the week.

    Attributes
    ----------
    MON : int
        Monday.
    TUE : int
        Tuesday.
    WED : int
        Wednesday.
    THU : int
        Thursday.
    FRI : int
        Friday.
    SAT : int
        Saturday.
    SUN : int
        Sunday.
    """

    MON = 1
    TUE = 2
    WED = 3
    THU = 4
    FRI = 5
    SAT = 6
    SUN = 7


class Month(enum.Enum):
    """
    Represents months of the year.

    Attributes
    ----------
    JAN : int
        January.
    FEB : int
        February.
    MAR : int
        March.
    APR : int
        April.
    MAY : int
        May.
    JUN : int
        June.
    JUL : int
        July.
    AUG : int
        August.
    SEP : int
        September.
    OCT : int
        October.
    NOV : int
        November.
    DEC : int
        December.
    """

    JAN = 1
    FEB = 2
    MAR = 3
    APR = 4
    MAY = 5
    JUN = 6
    JUL = 7
    AUG = 8
    SEP = 9
    OCT = 10
    NOV = 11
    DEC = 12


class IteratorType(enum.Enum):
    """
    Represents types of iterators.

    Attributes
    ----------
    TAG : str
        Tag iterator.
    PARAMETER : str
        Parameter iterator.
    """

    TAG = "tag"
    PARAMETER = "parameter"
