import abc
from typing import Union

from docutils.nodes import description

from onedata_wrapper.models.filesystem.entry_request import EntryRequest
from onedata_wrapper.models.filesystem.filesystem_entry import FilesystemEntry


class NewShareRequest(abc.ABC):
    """
    Class representing abstract New Share Request when creating Share in Onedata
    """
    def __init__(self, entry: Union[FilesystemEntry, EntryRequest], name: str, description: str = None):
        """
        :param entry: FilesystemEntry or EntryRequest representing the entry of which the share should be created
        :param name: String name of the new share
        :param description: Optional string description of the share
        :raises ValueError: if the entry was initialized incorrectly or new Share has no name
        """
        if entry.file_id is None:
            raise ValueError("FileId of FilesystemEntry or EntryRequest object was not set")
        if name is None:
            raise ValueError("Name of the new Share was not set")

        self._file_id = entry.file_id
        self._name = name
        self._description = description

    @property
    def name(self):
        """Name representing new Entry
        """
        return self._name

    @property
    def file_id(self):
        """Onedata FileId of entry of the new Share
        """
        return self._file_id

    @property
    def description(self):
        """Textual description of the Share
        """
        return self._description

    def request_attrs(self) -> dict[str, Union[str, bytes]]:
        attrs = {
            "name": self.name,
            "root_file_id": self.file_id,
        }
        if description is not None:
            attrs["description"] = self.description

        return attrs
