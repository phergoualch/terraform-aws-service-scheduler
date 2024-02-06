class Tag:
    """
    Represents a key-value pair used for tagging.

    Attributes
    ----------
    key : str
        The key of the tag.
    value : str
        The value associated with the tag.

    Methods
    -------
    __eq__(other)
        Compare the tag with another tag for equality.
    __repr__()
        Return a string representation of the tag.

    Examples
    --------
    Creating a Tag instance:

    >>> my_tag = Tag(key="Environment", value="Production")

    Comparing two tags for equality:

    >>> tag1 = Tag(key="Department", value="HR")
    >>> tag2 = Tag(key="Department", value="HR")
    >>> tag1 == tag2
    True

    String representation of a tag:

    >>> tag = Tag(key="Owner", value="John Doe")
    >>> repr(tag)
    'Tag(key=Owner, value=John Doe)'
    """

    def __init__(self, key: str, value: str):
        """
        Initialize a Tag instance.

        Parameters
        ----------
        key : str
            The key of the tag.
        value : str
            The value associated with the tag.
        """
        self.key = key
        self.value = value

    def __eq__(self, other):
        """
        Compare the tag with another tag for equality.

        Parameters
        ----------
        other : Tag
            The tag to compare with.

        Returns
        -------
        bool
            True if the tags are equal, False otherwise.
        """
        return self.__dict__ == other.__dict__

    def __repr__(self):
        """
        Return a string representation of the tag.

        Returns
        -------
        str
            A string representation of the tag.
        """
        return f"Tag(key={self.key}, value={self.value})"
