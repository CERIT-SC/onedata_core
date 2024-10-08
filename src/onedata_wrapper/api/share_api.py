
import oneprovider_client
from oneprovider_client.models.share_create_request import ShareCreateRequest
from oneprovider_client.configuration import Configuration as OneproviderConfiguration
from oneprovider_client.rest import ApiException

from onedata_wrapper.models.share.new_share_request import NewShareRequest
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
