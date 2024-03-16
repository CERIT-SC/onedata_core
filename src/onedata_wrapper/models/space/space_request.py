
class SpaceRequest(object):
    """
    Class representing a request to get info about Onedata Space.
    """
    def __init__(self, space_id: str):
        """
        :param space_id: Onedata SpaceId used for requesting the Space information
        :raises ValueError: if space_id is not a valid string value
        """
        if space_id is None or not isinstance(space_id, str):
            raise ValueError("Value for space_id must be set and must be string in order to initialize the object")
        self._space_id: str = space_id

    @property
    def space_id(self):
        """Onedata SpaceId
        """
        return self._space_id
