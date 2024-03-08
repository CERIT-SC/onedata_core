"""
This file provides a basic example how to use FileOperationsApi when the user knows file_id
"""

import oneprovider_client
from onedata_wrapper.api.file_operations_api import FileOperationsApi
from onedata_wrapper.models.filesystem.dir_entry import DirEntry
from onedata_wrapper.models.space.space_request import SpaceRequest

if __name__ == "__main__":
    oneprovider_configuration = oneprovider_client.configuration.Configuration()
    oneprovider_configuration.host = "https://BLINDED.muni.cz/api/v3/oneprovider"
    oneprovider_configuration.api_key['X-Auth-Token'] = "BLINDED"

    file_op_api = FileOperationsApi(oneprovider_configuration)

    space_request = SpaceRequest(space_id="BLINDED")
    space = file_op_api.get_space(space_request)
    print(space.space_id, space.name)
    file_op_api.get_root(space)

    basic_dir = space.root_dir
    file_op_api.get_children(basic_dir)

    for child in basic_dir.children:
        if isinstance(child, DirEntry):
            file_op_api.get_children(child)
            for child2 in child.children:
                if isinstance(child2, DirEntry):
                    file_op_api.get_children(child2)

    print(dict(basic_dir))
    for child in basic_dir.children:
        print(dict(child))
        if isinstance(child, DirEntry):
            for child2 in child.children:
                print(dict(child2))

