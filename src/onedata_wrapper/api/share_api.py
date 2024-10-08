
import oneprovider_client
from oneprovider_client.models.share_create_request import ShareCreateRequest
from oneprovider_client.configuration import Configuration as OneproviderConfiguration
from oneprovider_client.rest import ApiException

from onedata_wrapper.converters.share_converter import ShareConverter
from onedata_wrapper.models.filesystem.filesystem_entry import FilesystemEntry
from onedata_wrapper.models.share.new_share_request import NewShareRequest
from onedata_wrapper.models.share.share import Share
from onedata_wrapper.models.share.share_request import ShareRequest



class ShareApi(object):
    """
    Class representing Share API used as a facade pattern communicating with onedata-lib(s)
    doing share operations more accessible due to abstraction of concretes

    This part of the API uses models from models/filesystem package.
    Those are necessary to use, to use this API.
    """
    def __init__(self, configuration: OneproviderConfiguration):
        """
        :param configuration: OneproviderConfiguration from oneprovider_client library. Must be initialized.
        """
        self._configuration: OneproviderConfiguration = configuration

    def new_share(self, new_share_request: NewShareRequest) -> ShareRequest:
        """
        Creates new Share in Onedata using `new_share_request` and returns ShareRequest
        which can be later used for fetching more data about newly created Share

        In order this function to work,
        an actual user represented by token MUST HAVE caveats allowing the share creation
        ('space_manage_share')

        :param new_share_request: NewShareRequest object representing the Share to be created
        :return: ShareRequest object representing newly created Share which can be later used by get_share() function
        :raises IOError: if new Entry couldn't be created
        """
        parameters = new_share_request.request_attrs()

        api_instance = oneprovider_client.ShareApi(oneprovider_client.ApiClient(self._configuration))
        # https://onedata.org/#/home/api/stable/oneprovider?anchor=operation/create_share

        new_share = ShareCreateRequest(**parameters)

        try:
            # Create share
            api_response = api_instance.create_share(new_share)
        except ApiException as e:
            raise IOError("Could not create requested share") from e

        share_id = api_response.share_id

        share_request = ShareRequest(share_id)
        return share_request

    def get_share(self, share_request: ShareRequest) -> Share:
        """
        Returns Share represented by `share_request` object from Onedata.

        In order this function to work,
        an actual user represented by token MUST HAVE rights to access Share with specified ShareId

        :param share_request: ShareRequest object representing the file to be returned
        :return: Share represented by `share_request` with data fetched from Onedata
        :raises AttributeError: if `share_id` in `share_request` is not a valid ShareId in Onedata or any related error
        """
        api_instance = oneprovider_client.ShareApi(oneprovider_client.ApiClient(self._configuration))
        # https://onedata.org/#/home/api/stable/oneprovider?anchor=operation/get_share

        try:
            api_response = api_instance.get_share(share_request.share_id)
        except ApiException as e:
            raise AttributeError("Error with getting info about share with given Id") from e

        share = ShareConverter.convert(api_response)
        return share

    def fetch_shares(self, filesystem_entry: FilesystemEntry):
        """
        Fetches the share information using the share data stored in `filesystem_entry` object from Onedata.
        The Shares information is stored in the `filesystem_entry` object itself, replacing the older ShareRequest
        or Share objects list.
        Ability to fetch the info about the Share again is not a bug, but the feature (the data could have been changed)

        In order this function to work,
        an actual user represented by token MUST HAVE rights to access Share with specified ShareId

        :param filesystem_entry: FilesystemEntry representing an actual in the Onedata
        :return: List of the Share objects represented by `filesystem_entry.shares` with data fetched from Onedata
        :raises AttributeError: if `filesystem_entry` was not initialized with a shares FileAttribute
         or any related error
        """
        if filesystem_entry.shares is None:
            raise AttributeError("FilesystemEntry was initialized without info about Shares")

        shares = []
        for share_request in filesystem_entry.shares:
            fetched = self.get_share(share_request)
            shares.append(fetched)

        filesystem_entry.shares = shares
        return shares
