import abc
from typing import Union
from onedata_wrapper.models.filesystem.dir_entry import DirEntry
from onedata_wrapper.models.filesystem.entry_request import EntryRequest


class NewEntryRequest(abc.ABC):
    """
    Class representing abstract New Entry Request when creating Entry in Onedata
    """
    def __init__(self, parent: Union[DirEntry, EntryRequest], name: str, mode: int = 644):
        """
        :param parent: DirEntry or EntryRequest representing parent, in which new Entry will be created
        :param name: String name of the new entry
        :param mode: Optional int POSIX file mode; should be decimal value of three numbers, e.g. 644
        :raises ValueError: if parent was initialized incorrectly or new Entry has no name
        """
        if parent.file_id is None:
            raise ValueError("FileId of DirEntry or FilesystemEntry object was not set")
        if name is None:
            raise ValueError("Name of the new Entry was not set")

        self._file_id = parent.file_id
        self._name = name
        self._mode = mode

    @property
    def name(self):
        """Name representing new Entry
        """
        return self._name

    @property
    def mode(self):
        """POSIX Mode of new Entry
        """
        return self._mode

    @property
    def parent_id(self):
        """Onedata FileId of parent of the new Entry
        """
        return self._file_id

    def request_attrs(self) -> dict[str, Union[str, bytes]]:
        return {
            "name": self.name,
            "mode": self.mode,
            "id": self.parent_id
        }



