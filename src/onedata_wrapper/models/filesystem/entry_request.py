import abc


class EntryRequest(abc.ABC):
    """
    Class representing an Entry Request for accessing Filesystem Entry from Onedata

    This class is not an Entry on its own; it just holds information how to access real Entry
    """
    def __init__(self, file_id: str):
        """
        :param file_id: Onedata FileId used for requesting the FileEntry information
        :raises ValueError: if space_id is not a valid string value
        """
        if file_id is None or not isinstance(file_id, str):
            raise ValueError("Value for file_id must be set and must be string in order to initialize the object")
        self._file_id: str = file_id

    @property
    def file_id(self):
        """Onedata FileId
        """
        return self._file_id
