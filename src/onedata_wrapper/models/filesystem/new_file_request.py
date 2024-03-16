from typing import Optional, Union
from onedata_wrapper.models.filesystem.dir_entry import DirEntry
from onedata_wrapper.models.filesystem.entry_request import EntryRequest
from onedata_wrapper.models.filesystem.new_entry_request import NewEntryRequest


class NewFileRequest(NewEntryRequest):
    """
    Class representing New File Entry Request when creating Entry in Onedata

    Besides default parameters, NewFileEntry can also have `content` in bytes, which will be added to a new file
    """
    def __init__(self, parent: Union[DirEntry, EntryRequest], name: str, mode: int = 644,
                 contents: Optional[bytes] = None):
        self._contents = contents
        super().__init__(parent, name, mode)

    def request_attrs(self) -> dict[str, Union[str, bytes]]:
        out = super().request_attrs()
        additional = {
            "type": "REG"
        }
        out.update(additional)

        if self.contents is not None:
            out["body"] = self.contents

        return out

    @property
    def contents(self):
        """Contents of the new file
        """
        return self._contents
