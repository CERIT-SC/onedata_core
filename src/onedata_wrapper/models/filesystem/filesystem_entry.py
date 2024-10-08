import datetime
from typing import Optional
from abc import ABC

from onedata_wrapper.models.share.share import Share
from onedata_wrapper.models.share.share_request import ShareRequest


class FilesystemEntry(ABC):
    """
    Class representing Filesystem Entry in Onedata filesystem.

    Parameters are exact as what Onedata API returns
    """
    def __init__(self, name: str, file_id: str, mode=None, size=None, hard_links=None, atime=None, mtime=None, ctime=None,
                 owner_id=None, parent_id=None, provider_id=None, storage_user_id=None,
                 storage_group_id=None, shares=None, index=None):
        if name is None or file_id is None:
            raise ValueError("Filesystem Entry must have its own name and fileId")

        self._name: str = name
        self._file_id: str = file_id

        # preventing usage of redundant info
        # self.type = FilesystemEntry
        self._mode: Optional[str] = None

        self._size: Optional[int] = None
        self._hardlinks_count: Optional[int] = None
        self._atime: Optional[datetime.datetime] = None
        self._mtime: Optional[datetime.datetime] = None
        self._ctime: Optional[datetime.datetime] = None

        self._owner_id: Optional[str] = None
        self._parent_id: Optional[str] = None
        self._provider_id: Optional[str] = None
        self._storage_user_id: Optional[str] = None
        self._storage_group_id: Optional[str] = None

        self._shares: Optional[list[ShareRequest]] = None

        self._index: Optional[str] = None

        if mode is not None:
            self._mode = mode
        if size is not None:
            self._size = size
        if hard_links is not None:
            self._hardlinks_count = hard_links
        if atime is not None:
            self._atime = atime
        if mtime is not None:
            self._mtime = mtime
        if ctime is not None:
            self._ctime = ctime
        if owner_id is not None:
            self._owner_id = owner_id
        if parent_id is not None:
            self._parent_id = parent_id
        if provider_id is not None:
            self._provider_id = provider_id
        if storage_user_id is not None:
            self._storage_user_id = storage_user_id
        if storage_group_id is not None:
            self._storage_group_id = storage_group_id
        if shares is not None:
            self._shares = shares
        if index is not None:
            self._index = index

    def __iter__(self):
        yield "name", self._name
        yield "file_id", self._file_id
        yield "mode", self._mode
        yield "size", self._size
        yield "hard_links_count", self._hardlinks_count
        yield "atime", self._atime
        yield "mtime", self._mtime
        yield "ctime", self._ctime
        yield "owner_id", self._owner_id
        yield "parent_id", self._parent_id
        yield "provider_id", self._provider_id
        yield "storage_user_id", self._storage_user_id
        yield "storage_group_id", self._storage_group_id
        yield "shares", self._shares
        yield "index", self._index

    @property
    def name(self):
        """Name of the file
        """
        return self._name

    @property
    def file_id(self):
        """Onedata FileId
        """
        return self._file_id

    @property
    def mode(self):
        """POSIX file permissions in decimal format (e.g. 644, 700)
        """
        return self._mode

    @property
    def size(self):
        """Size of the file
        """
        return self._size

    @property
    def hardlinks_count(self):
        return self._hardlinks_count

    @property
    def atime(self):
        return self._atime

    @property
    def mtime(self):
        return self._mtime

    @property
    def ctime(self):
        return self._ctime

    @property
    def owner_id(self):
        return self._owner_id

    @property
    def parent_id(self):
        return self._parent_id

    @property
    def provider_id(self):
        return self._provider_id

    @property
    def storage_user_id(self):
        return self._storage_user_id

    @property
    def shares(self):
        return self._shares

    @shares.setter
    def shares(self, value: list[Share]):
        """Sets Share objects to actual FilesystemEntry instead of previous ShareRequests
        :raises ValueError: if Share objects are not in the correct format (list of a Share type
            with the same share ids)"""
        if not isinstance(self.shares, list):
            raise AttributeError("There were no shares at the object creation")

        if not isinstance(value, list):
            raise ValueError("Shares to set are not list")

        for share_new, share_old in zip(value, self.shares):
            if not isinstance(share_new, Share):
                raise ValueError("Share in the list is not a Share type")

            if share_new.share_id != share_old.share_id:
                raise ValueError("Share in the list does not correspond to the previous values")

        self._shares = value

    @property
    def index(self):
        return self._index
