import abc


class ShareRequest(abc.ABC):
    """
    Class representing a Share Request for accessing Share from Onedata

    This class is not a Share on its own; it just holds information how to access real Share
    """
    def __init__(self, share_id: str):
        """
        :param share_id: Onedata ShareId used for requesting the Share information
        :raises ValueError: if share_id is not a valid string value
        """
        if share_id is None or not isinstance(share_id, str):
            raise ValueError("Value for share_id must be set and must be string in order to initialize the object")
        self._share_id: str = share_id

    @property
    def share_id(self):
        """Onedata ShareId
        """
        return self._share_id
