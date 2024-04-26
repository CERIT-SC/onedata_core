from typing import Optional
from onedata_wrapper.models.filesystem.filesystem_entry import FilesystemEntry


class SymlinkEntry(FilesystemEntry):
    """
    Class representing Symbolic link Entry in Onedata filesystem.
    """
    def __init__(self, value: Optional[str], name: str, file_id: str, mode=None, size=None,
                 hard_links=None,
                 atime=None, mtime=None, ctime=None, owner_id=None, parent_id=None, provider_id=None,
                 storage_user_id=None, storage_group_id=None, shares=None, index=None):
        super().__init__(name, file_id, mode, size, hard_links, atime, mtime, ctime, owner_id, parent_id, provider_id,
                         storage_user_id, storage_group_id, shares, index)
        self._value: str = value

    def __iter__(self):
        yield from super().__iter__()
        yield "type", "SYMLNK"
        yield "symlink_value", self._value

    @property
    def value(self):
        """Symbolic link value of actual symlink
        :raises ValueError: if this property was called before setting the symlink value first
        """
        if self._value is None:
            raise ValueError("SymlinkEntry has not yet assigned value")
        return self._value

    @value.setter
    def value(self, value: str):
        """Sets symbolic link value to actual SymlinkEntry
        :raises ValueError: if symbolic link value is not in the correct format (str)"""
        if not isinstance(value, str):
            raise ValueError("Symbolic link value to set is not string")

        self._value = value
