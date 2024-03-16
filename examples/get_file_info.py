"""
This file provides a basic example how to use FileOperationsApi when the user knows file_id
"""

import oneprovider_client
from onedata_wrapper.api.file_operations_api import FileOperationsApi
from onedata_wrapper.models.filesystem.entry_request import EntryRequest
from onedata_wrapper.selectors.file_attribute import FileAttribute as FA

if __name__ == "__main__":
    # initialization of the configuration
    oneprovider_configuration = oneprovider_client.configuration.Configuration()
    oneprovider_configuration.host = "https://BLINDED.muni.cz/api/v3/oneprovider"
    oneprovider_configuration.api_key['X-Auth-Token'] = "BLINDED"

    # initialization of the library File Operations API
    file_op_api = FileOperationsApi(oneprovider_configuration)

    # creating EntryRequest object used for Entry retrieval based on FileId (not using API calls yet)
    entry_request = EntryRequest(file_id="BLINDED")

    # requesting Entry information from Onedata -> returns FileEntry, DirEntry or OtherEntry object based on a file type
    # requesting only owner_id and mode attributes of file to be returned, can be adjusted
    # (file_id, name and type is returned by default)
    requested_file = file_op_api.get_file(entry_request, FA.OWNER_ID | FA.MODE)

    # printing information using __iter__ function returning dict
    print(dict(requested_file))
