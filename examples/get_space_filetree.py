"""
This file provides a basic example how to use FileOperationsApi when the user knows space_id
"""

import oneprovider_client
from onedata_wrapper.api.file_operations_api import FileOperationsApi
from onedata_wrapper.models.filesystem.dir_entry import DirEntry
from onedata_wrapper.models.space.space_request import SpaceRequest
from onedata_wrapper.selectors.file_attribute import ALL as FA_ALL

if __name__ == "__main__":
    # initialization of the configuration
    oneprovider_configuration = oneprovider_client.configuration.Configuration()
    oneprovider_configuration.host = "https://BLINDED.muni.cz/api/v3/oneprovider"
    oneprovider_configuration.api_key['X-Auth-Token'] = "BLINDED"

    # initialization of the library File Operations API
    file_op_api = FileOperationsApi(oneprovider_configuration)

    # creating SpaceRequest object used for Space retrieval (not using API calls yet)
    space_request = SpaceRequest(space_id="BLINDED")
    # requesting Space information from Onedata
    space = file_op_api.get_space(space_request)
    # print(space.space_id, space.name)  # space info can be seen here
    # requesting information about Space root file
    file_op_api.get_root(space)

    # treating space root directory as usual directory
    basic_dir = space.root_dir
    # requesting children for actual directory from Onedata
    file_op_api.get_children(basic_dir, FA_ALL)

    # requesting children for two consecutive levels
    for child in basic_dir.children:
        if isinstance(child, DirEntry):
            file_op_api.get_children(child, FA_ALL)
            for child2 in child.children:
                if isinstance(child2, DirEntry):
                    file_op_api.get_children(child2, FA_ALL)

    # and printing information using __iter__ function returning dict
    print(dict(basic_dir))
    for child in basic_dir.children:
        print(dict(child))
        if isinstance(child, DirEntry):
            for child2 in child.children:
                print(dict(child2))
