from typing import Union
from onedata_wrapper.models.filesystem.new_entry_request import NewEntryRequest


class NewDirectoryRequest(NewEntryRequest):
    """
    Class representing New Directory Entry Request when creating Entry in Onedata
    """
    def request_attrs(self) -> dict[str, Union[str, bytes]]:
        out = super().request_attrs()
        additional = {
            "type": "DIR"
        }
        out.update(additional)
        return out
