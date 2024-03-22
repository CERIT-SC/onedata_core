import abc
from typing import Union
from onedata_wrapper.models.filesystem.dir_entry import DirEntry
from onedata_wrapper.models.filesystem.entry_request import EntryRequest


class NewSpaceRequest(abc.ABC):
    """
    Class representing abstract New Space Request when creating Space in Onedata
    """
    def __init__(self, name: str):
        """
        :param name: String name of the new space
        :raises ValueError: if new Space has no name
        """
        if name is None or not isinstance(name, str):
            raise ValueError("Name of the new Space was not set correctly")
        self._name = name

    @property
    def name(self):
        """Name representing new Space
        """
        return self._name

    def request_attrs(self) -> dict[str, Union[str, bytes]]:
        return {
            "name": self.name
        }



