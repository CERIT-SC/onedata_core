from datetime import datetime
from oneprovider_client.models.file_attributes import FileAttributes
from onedata_wrapper.converters.abstract_converter import AbstractConverter
from onedata_wrapper.models.filesystem.filesystem_entry import FilesystemEntry
from onedata_wrapper.models.filesystem.dir_entry import DirEntry
from onedata_wrapper.models.filesystem.other_entry import OtherEntry
from onedata_wrapper.models.filesystem.file_entry import FileEntry


class FileAttributesConverter(AbstractConverter):
    @staticmethod
    def convert(file_attributes: FileAttributes) -> FilesystemEntry:
        # changed
        entry_atime = None
        entry_mtime = None
        entry_ctime = None
        if file_attributes.atime is not None:
            entry_atime = datetime.fromtimestamp(file_attributes.atime)
        if file_attributes.mtime is not None:
            entry_mtime = datetime.fromtimestamp(file_attributes.mtime)
        if file_attributes.ctime is not None:
            entry_ctime = datetime.fromtimestamp(file_attributes.ctime)
        # unchanged
        entry_name = file_attributes.name
        entry_mode = file_attributes.mode
        entry_size = file_attributes.size
        entry_hardlinks = file_attributes.hardlinks_count
        entry_owner_id = file_attributes.owner_id
        entry_file_id = file_attributes.file_id
        entry_parent_id = file_attributes.parent_id
        entry_provider_id = file_attributes.provider_id
        entry_storage_user_id = file_attributes.storage_user_id
        entry_storage_group_id = file_attributes.storage_group_id
        entry_shares = file_attributes.shares
        entry_index = file_attributes.index

        common_attributes = (entry_name, entry_file_id, entry_mode, entry_size, entry_hardlinks,
                             entry_atime, entry_mtime, entry_ctime,
                             entry_owner_id, entry_parent_id, entry_provider_id, entry_storage_user_id,
                             entry_storage_group_id, entry_shares, entry_index)

        if file_attributes.type == "REG":
            entry = FileEntry(*common_attributes)
        elif file_attributes.type == "DIR":
            entry = DirEntry(None, *common_attributes)
        else:
            entry = OtherEntry(file_attributes.type, *common_attributes)

        return entry
