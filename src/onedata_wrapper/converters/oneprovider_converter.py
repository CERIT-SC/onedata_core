from oneprovider_client import Configuration as OneproviderConfiguration

from onedata_wrapper.converters.abstract_converter import AbstractConverter
from onedata_wrapper.models.service.oneprovider import Oneprovider


class OneproviderConverter(AbstractConverter):
    @staticmethod
    def convert(oneprovider_configuration: OneproviderConfiguration) -> Oneprovider:
        provider_id = oneprovider_configuration.provider_id
        name = oneprovider_configuration.name
        domain = oneprovider_configuration.domain
        onezone_domain = oneprovider_configuration.onezone_domain
        version = oneprovider_configuration.version
        build = oneprovider_configuration.build
        compatible_onezone_versions = oneprovider_configuration.compatible_onezone_versions
        compatible_oneprovider_versions = oneprovider_configuration.compatible_oneprovider_versions
        compatible_oneclient_versions = oneprovider_configuration.compatible_oneclient_versions

        oneprovider = Oneprovider(provider_id=provider_id, name=name, domain=domain, onezone_domain=onezone_domain,
                                  version=version, build=build, compatible_onezone_versions=compatible_onezone_versions,
                                  compatible_oneprovider_versions=compatible_oneprovider_versions,
                                  compatible_oneclient_versions=compatible_oneclient_versions)

        return oneprovider
