
class SpaceRequest:
    """
    Class representing a request to get info about Onedata Space.
    """
    def __init__(self, space_id: str):
        """
        :param space_id: Onedata SpaceId used for requesting the Space information
        """
        self._space_id: str = space_id

    @property
    def space_id(self):
        """Onedata SpaceId
        """
        return self._space_id
