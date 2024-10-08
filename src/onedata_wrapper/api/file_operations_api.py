from typing import Union

from oneprovider_client.configuration import Configuration as OneproviderConfiguration
import oneprovider_client
from oneprovider_client.rest import ApiException

from onedata_wrapper.api import oneprovider_api
from onedata_wrapper.api.oneprovider_api import OneproviderApi
from onedata_wrapper.models.filesystem.dir_entry import DirEntry
from onedata_wrapper.models.filesystem.filesystem_entry import FilesystemEntry
from onedata_wrapper.models.filesystem.entry_request import EntryRequest
from onedata_wrapper.models.filesystem.new_entry_request import NewEntryRequest
from onedata_wrapper.models.filesystem.symlink_entry import SymlinkEntry
from onedata_wrapper.models.space.space import Space
from onedata_wrapper.converters.directory_children_converter import DirectoryChildrenConverter
from onedata_wrapper.converters.file_attributes_converter import FileAttributesConverter
from onedata_wrapper.selectors.file_attribute import FileAttribute as FA


class FileOperationsApi(object):
    """
    Class representing File Operations API used as a facade pattern communicating with onedata-lib(s)
    doing file operations more accessible due to abstraction of concretes

    This part of the API uses models from models/filesystem package.
    Those are necessary to use, to use this API.
    """
    def __init__(self, configuration: OneproviderConfiguration):
        """
        :param configuration: OneproviderConfiguration from oneprovider_client library. Must be initialized.
        """
        self._configuration: OneproviderConfiguration = configuration

    def get_file(self, entry_request: EntryRequest, attributes: FA = FA.FILE_ID | FA.NAME) \
            -> FilesystemEntry:
        """
        Returns File represented by `entry_request` object from Onedata.

        In order this function to work,
        an actual user represented by token MUST HAVE rights to access Entry with specified FileId

        :param entry_request: EntryRequest object representing the file to be returned
        :param attributes: FileAttribute (from selectors) object representing values of Onedata Filesystem Entry
            to be included in the new returned object. Minimal requirement of `fileId`, `name` and `type`
            is added automatically
        :return: FilesystemEntry represented by `entry_request` with data fetched from Onedata
        :raises AttributeError: if `file_id` in `entry_request` is not a valid FileId in Onedata or any related error
        """
        api_instance = oneprovider_client.BasicFileOperationsApi(oneprovider_client.ApiClient(self._configuration))
        # https://onedata.org/#/home/api/stable/oneprovider?anchor=operation/get_attrs

        attribute = (attributes | FA.FILE_ID | FA.NAME | FA.TYPE).convert()
        # using kwargs instead of writing attributes directly allows to omit "token" in the first run

        # WARNING: multiple attributes not working, BUG in Onedata
        kwargs = {"attribute": attribute}

        try:
            # api_response = api_instance.get_attrs(space.root_dir.file_id, **kwargs)
            api_response = api_instance.get_attrs(entry_request.file_id)
        except ApiException as e:
            raise AttributeError("Error with getting info about file with given Id") from e

        fs_entry = FileAttributesConverter.convert(api_response)

        return fs_entry

    def get_children(self, directory: DirEntry, attributes: FA = FA.FILE_ID | FA.NAME) -> DirEntry:
        """
        Returns DirEntry provided using `directory` with updated children fetched from Onedata

        In the case of any error during children fetching, the old value of children is kept and not overwritten.
        Because of that, `directory` cannot be in inconsistent state.

        This function returns ALL CHILDREN of given directory.
        Because of that, a lot of objects could be created eating a lot of memory.

        In order this function to work,
        an actual user represented by token MUST HAVE rights to access parent DirEntry with specified FileId

        :param directory: DirEntry object representing the parent file children to be fetched and returned
        :param attributes: FileAttribute (from selectors) object representing values of Onedata Filesystem Entry
            to be included in the new returned object. Minimal requirement of `fileId`, `name` and `type`
            is added automatically
        :return: DirEntry with updated children fetched from Onedata
        :raises AttributeError: if children couldn't be fetched from Onedata or any related error
        """
        api_instance = oneprovider_client.BasicFileOperationsApi(oneprovider_client.ApiClient(self._configuration))
        # https://onedata.org/#/home/api/stable/oneprovider?anchor=operation/list_children

        attribute = (attributes | FA.FILE_ID | FA.NAME | FA.TYPE).convert()
        # using kwargs instead of writing attributes directly allows to omit "token" in the first run
        kwargs = {"attribute": attribute}

        directory_children = []

        while True:
            try:
                api_response = api_instance.list_children(directory.file_id, **kwargs)
            except ApiException as e:
                raise AttributeError("Error with getting children from FileId") from e

            children = DirectoryChildrenConverter.convert(api_response)

            directory_children.extend(children)

            if api_response.is_last:
                break
            kwargs["token"] = api_response.next_page_token

        directory.children = directory_children
        return directory

    def get_symlink_value(self, symlink: SymlinkEntry) -> SymlinkEntry:
        """
        Returns SymlinkEntry provided using `symlink` with updated value fetched from Onedata

        In order this function to work,
        an actual user represented by token MUST HAVE rights to access SymlinkEntry with specified FileId

        :param symlink: SymlinkEntry object representing the symbolic link vale of to be fetched
        :return: SymlinkEntry with updated value (symlink value) fetched from Onedata
        :raises AttributeError: if symbolic link value couldn't be fetched from Onedata or any related error
        """
        api_instance = oneprovider_client.BasicFileOperationsApi(oneprovider_client.ApiClient(self._configuration))
        # https://onedata.org/#/home/api/stable/oneprovider?anchor=operation/get_symlink_value

        try:
            api_response = api_instance.get_symlink_value(symlink.file_id)
        except ApiException as e:
            raise AttributeError("Error with getting symlink value from FileId") from e

        symlink.value = api_response

        return symlink

    def new_entry(self, new_entry_request: NewEntryRequest) -> EntryRequest:
        """
        Creates new Entry in Onedata using `new_entry_request` and returns EntryRequest
        which can be later used for fetching more data about newly created Entry

        In order this function to work,
        an actual user represented by token MUST HAVE caveats allowing the file creation
        and the filesystem on which operations are provided CANNOT BE read-only

        :param new_entry_request: NewEntryRequest object representing the Entry to be created
        :return: EntryRequest object representing newly created Entry which can be later used by get_file() function
        :raises IOError: if new Entry couldn't be created
        """
        parameters = new_entry_request.request_attrs()

        api_instance = oneprovider_client.BasicFileOperationsApi(oneprovider_client.ApiClient(self._configuration))
        # https://onedata.org/#/home/api/stable/oneprovider?anchor=operation/create_file

        # octet-stream expects body, but when working with directories, no body is provided
        # because of that, we simulate that there is some body
        if parameters.get("body") is None:
            parameters["body"] = b""

        try:
            # Create file in directory
            api_response = api_instance.create_file(**parameters)
        except ApiException as e:
            raise IOError("Could not create requested file") from e

        file_id = api_response.file_id

        fse_request = EntryRequest(file_id)
        return fse_request

    def get_root(self, space: Space, attributes: FA = FA.FILE_ID | FA.NAME) -> Space:
        """
        Returns Space provided using `space` with updated root fetched from Onedata

        Warning: This function changes the state of the Space object.
        If there is any try-catch mechanism for processing Exceptions, the Space object can be in inconsistent state
        and cannot be longer used.

        In order this function to work,
        an actual user represented by token MUST HAVE rights to access Space with specified SpaceId
        and its root file with specified FileOd

        :param space: Space object representing the Onedata Space which root should be fetched and returned
        :param attributes: FileAttribute (from selectors) object representing values of Onedata Filesystem Entry
            to be included in the new returned object. Minimal requirement of `fileId`, `name` and `type`
            is added automatically
        :return: Space with updated root directory
        :raises AttributeError: if root directory data couldn't be fetched from Onedata or any related error
        :raises TypeError:  if the returned root directory is not of a DirEntry type
        """
        # creates empty DirEntry, not needed to access _space_root_id
        space.initialize_root()

        root_dir_request = EntryRequest(file_id=space.root_dir.file_id)

        try:
            root_dir = self.get_file(root_dir_request, attributes=attributes)
        except ApiException as e:
            space.discard_root()
            raise AttributeError("Error with getting info about space's root directory") from e

        if not isinstance(root_dir, DirEntry):
            space.discard_root()
            raise TypeError("The root directory is expected to be of type DirEntry")

        space.reinit_root(root_dir)

        return space
