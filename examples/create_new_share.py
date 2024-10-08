"""
This file provides a basic example how to use ShareApi when creating new shares
"""

import oneprovider_client

from onedata_wrapper.api.share_api import ShareApi
from onedata_wrapper.models.filesystem.entry_request import EntryRequest
from onedata_wrapper.models.share.new_share_request import NewShareRequest

if __name__ == "__main__":
    # initialization of the configuration
    oneprovider_configuration = oneprovider_client.configuration.Configuration()
    oneprovider_configuration.host = "https://BLINDED.muni.cz/api/v3/oneprovider"
    oneprovider_configuration.api_key['X-Auth-Token'] = "BLINDED"

    # initialization of the library Share API
    share_api = ShareApi(oneprovider_configuration)

    # creating EntryRequest object used for reference of an Entry for a new Share (not using API calls yet)
    er = EntryRequest(file_id="BLINDED")

    # creating a new Onedata Share request
    # already initialized FilesystemEntry can also be used as an Entry reference
    # new share will have properties of name = New Share, description = This is a new share
    share = NewShareRequest(entry=er, name="New share", description="This is a new share")

    # requesting creation of the new share from Onedata -> returns ShareRequest latter usable
    new_share_request = share_api.new_share(share)

    # returned share request can be used to fetch the data about newly created share
    new_share = share_api.get_share(new_share_request)

    # printing information using __iter__ function returning dict
    print(dict(new_share))
