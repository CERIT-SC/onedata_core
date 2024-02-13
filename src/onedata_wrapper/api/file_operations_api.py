from oneprovider_client.configuration import Configuration as OneproviderConfiguration
from onedata_wrapper.converters.space_converter import SpaceConverter
from onedata_wrapper.models.filesystem.dir_entry import DirEntry
from onedata_wrapper.models.space.space import Space
import oneprovider_client
from oneprovider_client.rest import ApiException
from onedata_wrapper.converters.directory_children_converter import DirectoryChildrenConverter


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

        # using kwargs instead of writing attributes directly allows to omit "token" in the first run
        kwargs = {"attribute": attribute}

        while True:
            try:
                api_response = api_instance.list_children(directory.file_id, **kwargs)
            except ApiException as e:
                raise AttributeError("Error with getting children from FileId") from e

            children = DirectoryChildrenConverter.convert(api_response)

            actual_children = directory.children
            if actual_children is None:
                actual_children = []
            directory.children = actual_children + children

            if api_response.is_last:
                break
            kwargs["token"] = api_response.next_page_token

        return directory

    def get_space_info(self, space: Space) -> Space:
        if space.space_id is None:
            raise ValueError("SpaceId of Space object was not set")

        # create an instance of the API class
        api_instance = oneprovider_client.SpaceApi(oneprovider_client.ApiClient(self._configuration))
        sid = space.space_id

        try:
            # Get basic space information
            api_response = api_instance.get_space(sid)
        except ApiException as e:
            raise AttributeError("Error with getting space info from SpaceId") from e

        space = SpaceConverter.convert(api_response)
        return space
