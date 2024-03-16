from typing import Optional
from onedata_wrapper.models.filesystem.filesystem_entry import FilesystemEntry


class DirEntry(FilesystemEntry):
    """
    Class representing Directory Entry in Onedata filesystem.

    Besides default attributes, it contains a list of children of FilesystemEntry type

    :raises ValueError: When operations with children has failed
    """
    def __init__(self, children: Optional[list[FilesystemEntry]], name: str, file_id: str, mode=None, size=None, hard_links=None,
                 atime=None, mtime=None, ctime=None, owner_id=None, parent_id=None, provider_id=None,
                 storage_user_id=None, storage_group_id=None, shares=None, index=None):
        super().__init__(name, file_id, mode, size, hard_links, atime, mtime, ctime, owner_id, parent_id, provider_id,
                         storage_user_id, storage_group_id, shares, index)
        self._children: list[FilesystemEntry] = children

    def __iter__(self):
        yield from super().__iter__()
        yield "type", "DIR"
        yield "children", self._children

    @property
    def children(self):
        """Children of actual DirEntry
        :raises ValueError: if this property was called before setting the children first
        """
        if self._children is None:
            raise ValueError("DirEntry has not yet assigned children")
        return self._children

    @children.setter
    def children(self, value: list[FilesystemEntry]):
        """Sets children to actual DirEntry
        :raises ValueError: if children are not in the correct format (list of FilesystemEntry type)"""
        if not isinstance(value, list):
            raise ValueError("Children to set are not list")

        for child in value:
            if not isinstance(child, FilesystemEntry):
                raise ValueError("Child in children is not a FilesytemEntry type")

        self._children = value
