from oneprovider_client.configuration import Configuration as OneproviderConfiguration
from onedata_wrapper.converters.space_converter import SpaceConverter
from onedata_wrapper.models.filesystem.dir_entry import DirEntry
from onedata_wrapper.models.filesystem.filesystem_entry import FilesystemEntry
from onedata_wrapper.models.filesystem.filesystem_entry_request import FilesystemEntryRequest
from onedata_wrapper.models.filesystem.new_entry_request import NewEntryRequest
from onedata_wrapper.models.space.space import Space
import oneprovider_client
from oneprovider_client.rest import ApiException
from onedata_wrapper.converters.directory_children_converter import DirectoryChildrenConverter
from onedata_wrapper.converters.file_attributes_converter import FileAttributesConverter
from onedata_wrapper.models.space.space_request import SpaceRequest
from onedata_wrapper.selectors.file_attribute import FileAttribute as FA


class FileOperationsApi(object):
    def __init__(self, configuration: OneproviderConfiguration):
        self._configuration: OneproviderConfiguration = configuration

    def get_children(self, directory: DirEntry, attributes: FA = FA.FILE_ID | FA.NAME) -> DirEntry:
        if directory.file_id is None:
            raise ValueError("FileId of DirEntry object was not set")

        api_instance = oneprovider_client.BasicFileOperationsApi(oneprovider_client.ApiClient(self._configuration))
        # https://onedata.org/#/home/api/stable/oneprovider?anchor=operation/list_children

        attribute = (attributes | FA.TYPE).convert()
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

    def get_space(self, space_request: SpaceRequest) -> Space:
        if space_request.space_id is None:
            raise ValueError("SpaceId of Space object was not set")

        # create an instance of the API class
        api_instance = oneprovider_client.SpaceApi(oneprovider_client.ApiClient(self._configuration))
        sid = space_request.space_id

        try:
            # Get basic space information
            api_response = api_instance.get_space(sid)
        except ApiException as e:
            raise AttributeError("Error with getting space info from SpaceId") from e

        space_request = SpaceConverter.convert(api_response)
        return space_request

    def get_file(self, fs_entry_request: FilesystemEntryRequest, attributes: FA = FA.FILE_ID | FA.NAME) \
            -> FilesystemEntry:
        if fs_entry_request.file_id is None:
            raise ValueError("FileId of FilesystemEntry object was not set")

        api_instance = oneprovider_client.BasicFileOperationsApi(oneprovider_client.ApiClient(self._configuration))
        # https://onedata.org/#/home/api/stable/oneprovider?anchor=operation/get_attrs

        attribute = (attributes | FA.TYPE).convert()
        # using kwargs instead of writing attributes directly allows to omit "token" in the first run

        # WARNING: multiple attributes not working, BUG in Onedata
        kwargs = {"attribute": attribute}

        try:
            # api_response = api_instance.get_attrs(space.root_dir.file_id, **kwargs)
            api_response = api_instance.get_attrs(fs_entry_request.file_id)
        except ApiException as e:
            raise AttributeError("Error with getting info about file with given Id") from e

        fs_entry = FileAttributesConverter.convert(api_response)

        return fs_entry

    def get_root(self, space: Space, attributes: FA = FA.FILE_ID | FA.NAME):
        space.initialize_root()  # creates empty DirEntry, not needed to access _space_root_id

        if space.root_dir is None or space.root_dir.file_id is None:
            raise ValueError("RootDir of Space object was not set, Space not initialized properly")

        root_dir_request = FilesystemEntryRequest(file_id=space.root_dir.file_id)

        try:
            root_dir = self.get_file(root_dir_request, attributes=attributes)
        except ApiException as e:
            space.discard_root()
            raise AttributeError("Error with getting info about space's root directory") from e

        if not isinstance(root_dir, DirEntry):
            raise TypeError("The root directory is expected to be of type DirEntry")

        space.reinit_root(root_dir)

    def new_entry(self, entry_request: NewEntryRequest) -> FilesystemEntryRequest:
        parameters = entry_request.request_attrs()

        api_instance = oneprovider_client.BasicFileOperationsApi(oneprovider_client.ApiClient(self._configuration))

        # octet-stream expects body, but when working with directories, no body is provided
        # because of that, we simulate that there is some body
        if parameters.get("body") is None:
            parameters["body"] = b""

        try:
            # Create file in directory
            api_response = api_instance.create_file(**parameters)
        except ApiException as e:
            raise IOError("Could not create requested file") from e

        file_id = api_response.get("fileId")

        fse_request = FilesystemEntryRequest(file_id)
        return fse_request
