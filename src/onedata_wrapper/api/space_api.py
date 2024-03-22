import onezone_client
from oneprovider_client.configuration import Configuration as OneproviderConfiguration
from onezone_client.configuration import Configuration as OnezoneConfiguration
import oneprovider_client
from oneprovider_client.rest import ApiException
from onedata_wrapper.converters.space_converter import SpaceConverter
from onedata_wrapper.models.space.new_admin_space_request import NewAdminSpaceRequest
from onedata_wrapper.models.space.new_group_space_request import NewGroupSpaceRequest
from onedata_wrapper.models.space.new_space_request import NewSpaceRequest
from onedata_wrapper.models.space.new_user_space_request import NewUserSpaceRequest
from onedata_wrapper.models.space.space import Space
from onedata_wrapper.models.space.space_request import SpaceRequest


class SpaceApi(object):
    def __init__(self, onezone_configuration: OnezoneConfiguration = None,
                 oneprovider_configuration: OneproviderConfiguration = None):
        """
        :param onezone_configuration: OnezoneConfiguration from onezone_client library. (Optional)
        :param oneprovider_configuration: OneproviderConfiguration from oneprovider_client library. (Optional)

        :exception AttributeError: if there was not a single configuration provided
        :exception TypeError: if the specific configuration os not of the right type
        """
        if oneprovider_configuration is None and onezone_configuration is None:
            raise AttributeError("At least one of the configurations (o_provider, o_zone) must be provided")

        if onezone_configuration is not None and not isinstance(onezone_configuration, OnezoneConfiguration):
            raise TypeError("Onezone configuration is not of the right type")
        if oneprovider_configuration is not None and not isinstance(oneprovider_configuration, OneproviderConfiguration):
            raise TypeError("Oneprovider configuration is not of the right type")

        self._zone_conf: OnezoneConfiguration = onezone_configuration
        self._provider_conf: OneproviderConfiguration = oneprovider_configuration

    def get_space(self, space_request: SpaceRequest) -> Space:
        """
        Returns Space represented by `space_request` object from Onedata.

        In order this function to work,
        an actual user represented by token MUST HAVE rights to access Space with specified SpaceId

        :param space_request: SpaceRequest object representing the space to be returned
        :return: Space represented by `space_request` with data fetched from Onedata
        :raises AttributeError: if `space_id` in `entry_request` is not a valid SpaceId in Onedata or any related error
        """
        # create an instance of the API class
        api_instance = oneprovider_client.SpaceApi(oneprovider_client.ApiClient(self._provider_conf))
        sid = space_request.space_id

        try:
            # Get basic space information
            api_response = api_instance.get_space(sid)
        except ApiException as e:
            raise AttributeError("Error with getting space info from SpaceId") from e

        space_request = SpaceConverter.convert(api_response)
        return space_request

    def _new_admin_space(self, new_admin_space_request: NewAdminSpaceRequest):
        api_instance = onezone_client.SpaceApi(onezone_client.ApiClient(self._zone_conf))
        # https://onedata.org/#/home/api/stable/onezone?anchor=operation/create_space
        parameters = new_admin_space_request.request_attrs()

        body = onezone_client.SpacesBody(**parameters)

        try:
            api_response = api_instance.create_space(body=body)
        except ApiException as e:
            raise AttributeError("Error when creating Admin Space") from e

        pass

    def _new_group_space(self, new_group_space_request: NewGroupSpaceRequest):
        api_instance = onezone_client.GroupApi(onezone_client.ApiClient(self._zone_conf))
        # https://onedata.org/#/home/api/stable/onezone?anchor=operation/create_space_for_group

        parameters = new_group_space_request.request_attrs()
        group_id = parameters["id"]
        del parameters["id"]

        body = onezone_client.IdSpacesBody(**parameters)

        try:
            api_response = api_instance.create_space_for_group(group_id, body=body, _return_http_data_only=False)
        except ApiException as e:
            raise AttributeError("Error when creating Group Space") from e

        pass

    def _new_user_space(self, new_user_space_request: NewUserSpaceRequest):
        api_instance = onezone_client.UserApi(onezone_client.ApiClient(self._zone_conf))
        # https://onedata.org/#/home/api/stable/onezone?anchor=operation/create_user_space

        parameters = new_user_space_request.request_attrs()
        body = onezone_client.SpaceCreateRequest(**parameters)

        try:
            api_response = api_instance.create_user_space(body)
        except ApiException as e:
            raise AttributeError("Error when creating User Space") from e

        pass

    def new_space(self, new_space_request: NewSpaceRequest):
        if isinstance(new_space_request, NewAdminSpaceRequest):
            return self._new_admin_space(new_space_request)
        elif isinstance(new_space_request, NewGroupSpaceRequest):
            return self._new_group_space(new_space_request)
        elif isinstance(new_space_request, NewUserSpaceRequest):
            return self._new_user_space(new_space_request)
        else:
            raise TypeError("New Space Request must be of type NewSpaceRequest")
