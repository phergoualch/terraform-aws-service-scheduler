from models.enums import IteratorType


class Iterator:
    """
    Represents an iterator with an associated type.

    Parameters
    ----------
    iterator : int
        The iterator value.
    type : IteratorType
        The type of the iterator (DEFAULT or other).

    Attributes
    ----------
    iterator : int
        The iterator value.
    type : IteratorType
        The type of the iterator.

    Methods
    -------
    __repr__():
        Return a string representation of the Iterator object.
    __eq__(other):
        Compare this Iterator object with another for equality.
    __hash__():
        Return a hash value for the Iterator object.
    __lt__(other):
        Compare this Iterator object with another to determine order.

    Examples
    --------
    iterator = Iterator(1, IteratorType.DEFAULT)
    print(iterator)
    # Output: Iterator(iterator=1, type=DEFAULT)

    iterator1 = Iterator(1, IteratorType.DEFAULT)
    iterator2 = Iterator(2, IteratorType.OTHER)
    assert iterator1 == iterator2
    """

    def __init__(self, iterator: int, type: IteratorType):
        """
        Initialize an Iterator object with the specified iterator value and type.

        Parameters
        ----------
        iterator : int
            The iterator value.
        type : IteratorType
            The type of the iterator (DEFAULT or other).
        """
        self.iterator = iterator
        self.type = type

    def __repr__(self):
        """
        Return a string representation of the Iterator object.

        Returns
        -------
        str
            String representation of the Iterator object.
        """
        return f"Iterator(iterator={self.iterator}, type={self.type})"

    def __eq__(self, other):
        """
        Compare this Iterator object with another for equality.

        Parameters
        ----------
        other : Iterator
            Another Iterator object for comparison.

        Returns
        -------
        bool
            True if the two Iterator objects are equal, False otherwise.
        """
        return self.iterator == other.iterator and self.type == other.type

    def __hash__(self) -> int:
        """
        Return a hash value for the Iterator object.

        Returns
        -------
        int
            Hash value for the Iterator object.
        """
        return hash((self.iterator, self.type))

    def __lt__(self, other):
        """
        Compare this Iterator object with another to determine order.

        Parameters
        ----------
        other : Iterator
            Another Iterator object for comparison.

        Returns
        -------
        bool
            True if this Iterator object is less than the other, False otherwise.
        """
        if self.iterator == None:
            return True
        elif other.iterator == None:
            return False
        else:
            return self.iterator < other.iterator
