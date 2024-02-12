from abc import ABC


class EntryRequest(ABC):
    def __init__(self, file_id: str):
        self._file_id = None

        if file_id is not None:
            self._file_id = file_id

    @property
    def file_id(self):
        return self._file_id
