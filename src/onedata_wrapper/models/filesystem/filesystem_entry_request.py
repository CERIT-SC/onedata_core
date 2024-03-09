
class FilesystemEntryRequest:
    def __init__(self, file_id: str):
        self._file_id: str = file_id

    @property
    def file_id(self):
        return self._file_id
