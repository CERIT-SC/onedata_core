"""
This file provides a basic example how to use FileOperationsApi when creating new files or directories
"""

import oneprovider_client
from onedata_wrapper.api.file_operations_api import FileOperationsApi
from onedata_wrapper.models.filesystem.entry_request import EntryRequest
from onedata_wrapper.models.filesystem.new_file_request import NewFileRequest
from onedata_wrapper.selectors.file_attribute import ALL as FA_ALL

if __name__ == "__main__":
    # initialization of the configuration
    oneprovider_configuration = oneprovider_client.configuration.Configuration()
    oneprovider_configuration.host = "https://BLINDED.muni.cz/api/v3/oneprovider"
    oneprovider_configuration.api_key['X-Auth-Token'] = "BLINDED"

    # initialization of the library File Operations API
    file_op_api = FileOperationsApi(oneprovider_configuration)

    # creating EntryRequest object used for parental reference for a new Entry (not using API calls yet)
    # provided FileId must represent a directory, otherwise new entry cannot be created
    parent_er = EntryRequest(file_id="BLINDED")

    # creating a new Onedata filesystem Entry request
    # already initialized DirEntry can also be used as parental reference
    # new file will have properties of name = new_file.txt, POSIX mode = 600 (owner read/write) and contents = b-text
    file_request = NewFileRequest(parent=parent_er, name="new_file.txt", mode=600, contents=b"Really confidential info")

    # directory request can be created similarly
    # dir_request = NewDirectoryRequest(parent=parent_er, name="new_dir")

    # requesting creation of the new entry from Onedata -> returns EntryRequest latter usable
    newfile_entry_request = file_op_api.new_entry(file_request)

    # returned entry request can be used to fetch all information about newly created file
    new_file = file_op_api.get_file(newfile_entry_request, FA_ALL)

    # printing information using __iter__ function returning dict
    print(dict(new_file))
