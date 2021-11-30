class League:
    """
    A container for storing league url as well as league name.

    Attributes
    ----------

    Methods
    -------
        __init__(self, url, name):
            Initializes the attributes.
    """

    def __init__(self, url, name):
        """
        Initializes the attributes.

        :return: The object itself
        """

        self.url = url
        self.name = name
