from typing import Union, Optional

from onedata_wrapper.models.filesystem.dir_entry import DirEntry
from onedata_wrapper.models.filesystem.entry_request import EntryRequest
from onedata_wrapper.models.filesystem.new_entry_request import NewEntryRequest


class NewDirectoryRequest(NewEntryRequest):
    def __init__(self, parent: Union[DirEntry, EntryRequest], name: str, mode: int = 0o0644):
        super().__init__(parent, name, mode)

    def request_attrs(self) -> dict[str, str]:
        out = super().request_attrs()
        additional = {
            "type": "DIR"
        }
        out.update(additional)
        return out
