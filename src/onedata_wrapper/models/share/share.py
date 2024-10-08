from typing import Optional
from abc import ABC

from onedata_wrapper.models.filesystem.entry_request import EntryRequest
from onedata_wrapper.models.space.space_request import SpaceRequest


class Share(ABC):
    """
    Class representing a Share in Onedata filesystem.

    Parameters are exact as what Onedata API returns
    """
    def __init__(self, share_id: str, name:str, description:str, public_url:str, space_id:str, root_file_id:str,
                 root_file_type:str, handle_id=None):
        if None in (share_id, name, description, public_url, space_id, root_file_id, root_file_type):
            raise ValueError("Share must have its required fields filled out")

        self._share_id:str = share_id
        self._name:str = name
        self._description:str = description
        self._public_url:str = public_url

        self._space_id:str = space_id
        self._space: SpaceRequest = SpaceRequest(space_id=self._space_id)

        self._root_file_id:str = root_file_id
        self._root_file: EntryRequest = EntryRequest(file_id=self._root_file_id)

        self._root_file_type:str = root_file_type

        self._handle_id: Optional[str] = None

        if handle_id is not None:
            self._handle_id = handle_id

    def __iter__(self):
        yield "share_id", self._share_id
        yield "name", self._name
        yield "description", self._description
        yield "public_url", self._public_url
        yield "space_id", self._space_id
        yield "root_file_id", self._root_file_id
        yield "root_file_type", self._root_file_type
        yield "handle_id", self._handle_id

    @property
    def name(self):
        """Name of the share
        """
        return self._name

    @property
    def share_id(self):
        """Onedata ShareId
        """
        return self._share_id

    @property
    def description(self):
        return self._description

    @property
    def public_url(self):
        return self._public_url

    @property
    def space_id(self):
        return self._space_id

    @property
    def space(self):
        return self._space

    @property
    def root_file_id(self):
        return self._root_file_id

    @property
    def root_file(self):
        return self._root_file

    @property
    def root_file_type(self):
        return self._root_file_type

    @property
    def handle_id(self):
        return self._handle_id
