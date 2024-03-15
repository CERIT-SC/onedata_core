from typing import Optional
from onedata_wrapper.models.filesystem.filesystem_entry import FilesystemEntry


class DirEntry(FilesystemEntry):
    def __init__(self, children: list[FilesystemEntry] = None, name=None, mode=None, size=None, hard_links=None,
                 atime=None, mtime=None, ctime=None, owner_id=None, file_id=None, parent_id=None, provider_id=None,
    def __init__(self, children: Optional[list[FilesystemEntry]], name: str, file_id: str, mode=None, size=None, hard_links=None,
                 atime=None, mtime=None, ctime=None, owner_id=None, parent_id=None, provider_id=None,
                 storage_user_id=None, storage_group_id=None, shares=None, index=None):
        super().__init__(name, mode, size, hard_links, atime, mtime, ctime, owner_id, file_id, parent_id, provider_id,
                         storage_user_id, storage_group_id, shares, index)
        self._children: list[FilesystemEntry] = children

    def __iter__(self):
        yield from super().__iter__()
        yield "type", "DIR"
        yield "children", self._children

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, value: list[FilesystemEntry]):
        if not isinstance(value, list):
            raise ValueError("Children to set are not list")

        for child in value:
            if not isinstance(child, FilesystemEntry):
                raise ValueError("Child in children is not a FilesytemEntry type")

        self._children = value
