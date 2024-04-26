import oneprovider_client
from oneprovider_client.configuration import Configuration as OneproviderConfiguration
from oneprovider_client.rest import ApiException as OneproviderApiException
from onedata_wrapper.converters.oneprovider_converter import OneproviderConverter


class OneproviderApi(object):
    """
    Class representing Oneprovider API used as a facade pattern communicating with onedata-lib(s)
    doing oneprovider operations more accessible due to abstraction of concretes

    This part of the API uses models from models/service package.
    Those are necessary to use, to use this API.
    """
    @staticmethod
    def get_info(configuration: OneproviderConfiguration):
        """
        :param configuration: OneproviderConfiguration from oneprovider_client library. Must be initialized.
        """
        api_instance = oneprovider_client.OneproviderApi(oneprovider_client.ApiClient(configuration))

        try:
            api_response = api_instance.get_configuration()
        except OneproviderApiException as e:
            raise AttributeError("Error with getting info about current Oneprovider") from e

        oneprovider = OneproviderConverter.convert(api_response)
        return oneprovider
