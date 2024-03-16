import abc


class EntryRequest(abc.ABC):
    def __init__(self, file_id: str):
        if file_id is None or not isinstance(file_id, str):
            raise ValueError("Value for file_id must be set and must be string in order to initialize the object")
        self._file_id: str = file_id

    @property
    def file_id(self):
        return self._file_id
