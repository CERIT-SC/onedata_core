from oneprovider_client.configuration import Configuration as OneproviderConfiguration
from models.dir_entry import DirEntry
import oneprovider_client
from oneprovider_client.rest import ApiException
from converters.directory_children_converter import DirectoryChildrenConverter


class FileOperationsApi(object):
    def __init__(self, configuration: OneproviderConfiguration):
        self._configuration: OneproviderConfiguration = configuration

    def get_children(self, directory: DirEntry) -> DirEntry:
        if directory.file_id is None:
            raise ValueError("FileId of DirEntry object was not set")

        api_instance = oneprovider_client.BasicFileOperationsApi(oneprovider_client.ApiClient(self._configuration))
        # https://onedata.org/#/home/api/stable/oneprovider?anchor=operation/list_children
        attribute = ["name", "owner_id", "type", "mode", "size", "atime", "mtime", "ctime", "storage_group_id",
                     "storage_user_id", "shares", "provider_id", "file_id", "parent_id", "hardlinks_count",
                     "index"]

        try:
            api_response = api_instance.list_children(directory.file_id, attribute=attribute)
        except ApiException as e:
            raise AttributeError("Error with getting children from FileId") from e

        while True:
            children = DirectoryChildrenConverter.convert(api_response)

            actual_children = directory.children
            if actual_children is None:
                actual_children = []
            directory.children = actual_children + children

            if api_response.is_last:
                break
            token = api_response.token

            try:
                api_response = api_instance.list_children(directory.file_id, attribute=attribute, token=token)
            except ApiException as e:
                raise AttributeError("Error with getting children from FileId") from e

        return directory
