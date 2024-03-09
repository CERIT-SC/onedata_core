import abc
from typing import Union, Optional

from onedata_wrapper.models.filesystem.dir_entry import DirEntry
from onedata_wrapper.models.filesystem.entry_request import EntryRequest


class NewEntryRequest(abc.ABC):

    def __init__(self, parent: Union[DirEntry, EntryRequest], name: str, mode: int = 0o0644):
        if parent.file_id is None:
            raise ValueError("FileId of DirEntry or FilesystemEntry object was not set")

        self._file_id = parent.file_id
        self._name = name
        self._mode = mode

    @property
    def name(self):
        return self._name

    @property
    def mode(self):
        return self._mode

    @property
    def parent_id(self):
        return self._file_id

    def request_attrs(self) -> dict[str, str]:
        return {
            "name": self.name,
            "mode": self.mode,
            "id": self.parent_id
        }



