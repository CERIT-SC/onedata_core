from typing import Optional
from onedata_wrapper.models.filesystem.filesystem_entry import FilesystemEntry


class FileEntry(FilesystemEntry):
    """
    Class representing File Entry in Onedata filesystem.
    """
    pass

    def __iter__(self):
        yield from super().__iter__()
        yield "type", "REG"

