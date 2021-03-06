class Club:
    """
    A container for storing club id as well as club name.

    Attributes
    ----------

    Methods
    -------
        __init__(self, club_id, name):
            Initializes the attributes.
    """

    def __init__(self, club_id, name, league):
        """
        Initializes the attributes.

        :return: The object itself
        """

        self.club_id = club_id
        self.name = name
        self.league = league
