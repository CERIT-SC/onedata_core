
class Oneprovider:
    def __init__(self, provider_id: str, name: str, domain: str, onezone_domain: str, version: str, build: str,
                 compatible_onezone_versions: list[str], compatible_oneprovider_versions: list[str],
                 compatible_oneclient_versions: list[str]):
        if (provider_id is None or name is None or domain is None or onezone_domain is None
                or version is None or build is None or compatible_onezone_versions is None
                or compatible_oneprovider_versions is None or compatible_oneclient_versions is None):

            raise ValueError("Oneprovider does not contain all required values on creation")

        self._provider_id = provider_id
        self._name = name
        self._domain = domain
        self._onezone_domain = onezone_domain
        self._version = version
        self._build = build
        self._compatible_onezone_versions = compatible_onezone_versions
        self._compatible_oneprovider_versions = compatible_oneprovider_versions
        self._compatible_oneclient_versions = compatible_oneclient_versions

    @property
    def name(self):
        return self._name

    @property
    def provider_id(self):
        return self._provider_id

    @property
    def domain(self):
        return self._domain

    @property
    def onezone_domain(self):
        return self._onezone_domain

    @property
    def version(self):
        return self._version

    @property
    def build(self):
        return self._build

    @property
    def compatible_onezone_versions(self):
        return self._compatible_onezone_versions

    @property
    def compatible_oneprovider_versions(self):
        return self._name

    @property
    def compatible_oneclient_versions(self):
        return self._compatible_oneclient_versions
