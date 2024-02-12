from typing import Optional
from .filesystem_entry import FilesystemEntry


class OtherEntry(FilesystemEntry):
    def __init__(self, entry_type: str, name=None, mode=None, size=None, hard_links=None, atime=None, mtime=None,
                 ctime=None, owner_id=None, file_id=None, parent_id=None, provider_id=None, storage_user_id=None,
                 storage_group_id=None, shares=None, index=None):
        super().__init__(name, mode, size, hard_links, atime, mtime, ctime, owner_id, file_id, parent_id, provider_id,
                         storage_user_id, storage_group_id, shares, index)
        self._type = entry_type

    def __iter__(self):
        yield from super().__iter__()
        yield "type", self._type

    @property
    def type(self):
        return self._type
