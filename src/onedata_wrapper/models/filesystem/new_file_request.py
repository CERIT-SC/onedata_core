from typing import Optional, Union

from onedata_wrapper.models.filesystem.dir_entry import DirEntry
from onedata_wrapper.models.filesystem.entry_request import EntryRequest
from onedata_wrapper.models.filesystem.new_entry_request import NewEntryRequest


class NewFileRequest(NewEntryRequest):
    def __init__(self, parent: Union[DirEntry, EntryRequest], name: str, mode: int = 0o0644,
                 contents: Optional[bytes] = None):
        self._contents = contents
        super().__init__(parent, name, mode)

    def request_attrs(self) -> dict[str, str]:
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
        return self._contents
