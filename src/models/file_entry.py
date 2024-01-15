from typing import Optional
from .filesystem_entry import FilesystemEntry


class FileEntry(FilesystemEntry):
    pass

    def __iter__(self):
        yield from super().__iter__()
        yield "type", "REG"

