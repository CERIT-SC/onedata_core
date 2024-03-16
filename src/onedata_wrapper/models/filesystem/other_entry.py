from typing import Optional
from onedata_wrapper.models.filesystem.filesystem_entry import FilesystemEntry


class OtherEntry(FilesystemEntry):
    """
    Class representing another type of Entry in Onedata filesystem.

    Besides default attributes, it contains an attribute representing an Entry type in Onedata syntax
    """
    def __init__(self, entry_type: str, name: str, file_id: str, mode=None, size=None, hard_links=None, atime=None, mtime=None,
                 ctime=None, owner_id=None, parent_id=None, provider_id=None, storage_user_id=None,
                 storage_group_id=None, shares=None, index=None):
        super().__init__(name, file_id, mode, size, hard_links, atime, mtime, ctime, owner_id, parent_id, provider_id,
                         storage_user_id, storage_group_id, shares, index)
        self._type = entry_type

    def __iter__(self):
        yield from super().__iter__()
        yield "type", self._type

    @property
    def type(self):
        """Onedata type
        """
        return self._type
