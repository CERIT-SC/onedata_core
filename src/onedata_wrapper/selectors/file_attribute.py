from enum import auto
from onedata_wrapper.selectors.abstract_selector import AbstractSelector


class FileAttribute(AbstractSelector):
    NAME = auto()
    OWNER_ID = auto()
    TYPE = auto()
    MODE = auto()
    SIZE = auto()
    ATIME = auto()
    MTIME = auto()
    CTIME = auto()
    STORAGE_GROUP_ID = auto()
    STORAGE_USER_ID = auto()
    SHARES = auto()
    PROVIDER_ID = auto()
    FILE_ID = auto()
    PARENT_ID = auto()
    HARDLINKS_COUNT = auto()
    INDEX = auto()

    def convert(self, _=None):
        return super().convert(_conversion_table)


_conversion_table = {
    FileAttribute.NAME: "name",
    FileAttribute.OWNER_ID: "owner_id",
    FileAttribute.TYPE: "type",
    FileAttribute.MODE: "mode",
    FileAttribute.SIZE: "size",
    FileAttribute.ATIME: "atime",
    FileAttribute.MTIME: "mtime",
    FileAttribute.CTIME: "ctime",
    FileAttribute.STORAGE_GROUP_ID: "storage_group_id",
    FileAttribute.STORAGE_USER_ID: "storage_user_id",
    FileAttribute.SHARES: "shares",
    FileAttribute.PROVIDER_ID: "provider_id",
    FileAttribute.FILE_ID: "file_id",
    FileAttribute.PARENT_ID: "parent_id",
    FileAttribute.HARDLINKS_COUNT: "hardlinks_count",
    FileAttribute.INDEX: "index"
}

ALL = (FileAttribute.NAME | FileAttribute.OWNER_ID | FileAttribute.TYPE | FileAttribute.MODE | FileAttribute.SIZE
       | FileAttribute.ATIME | FileAttribute.MTIME | FileAttribute.CTIME | FileAttribute.STORAGE_GROUP_ID
       | FileAttribute.STORAGE_USER_ID | FileAttribute.SHARES | FileAttribute.PROVIDER_ID | FileAttribute.FILE_ID
       | FileAttribute.PARENT_ID | FileAttribute.HARDLINKS_COUNT | FileAttribute.INDEX)
