from __future__ import print_function

import json
import os
import time
from string import Template
import flask
import oneprovider_client
from flask import Blueprint, request
import onezone_client
import onepanel_client
from onezone_client.rest import ApiException as ApiExceptionZone
from onepanel_client.rest import ApiException as ApiExceptionPanel
from oneprovider_client.rest import ApiException as ApiExceptionProvider
from pprint import pprint
from utils import filesystem

space_bp = Blueprint('space', __name__, url_prefix='/space', static_folder="../static")


def create_metadata_md(space_name: str, institution_name: str, file_id: str, metadata_path: str) -> str:
    metadata_section = filesystem.read_file_contents(metadata_path)
    to_substitute = {
        "dataset_name": space_name,
        "institution_name": institution_name,
        "share_file_id": file_id,
        "metadata_section": metadata_section
    }
    template = filesystem.read_file_contents("data/templates/share_description.md")
    src = Template("".join(template))
    result = src.substitute(to_substitute)

    return result


@space_bp.route("/", methods=["GET"])
def get():
    return "Return from example GET"


@space_bp.route("/create", methods=["POST"])
def post():
    onezone_configuration = onezone_client.configuration.Configuration()
    onezone_configuration.host = "https://BLINDED.muni.cz/api/v3/onezone"
    onezone_configuration.api_key['X-Auth-Token'] = "BLINDED"

    onepanel_configuration = onepanel_client.configuration.Configuration()
    onepanel_configuration.host = "https://BLINDED.muni.cz/api/v3/onepanel"
    onepanel_configuration.api_key['X-Auth-Token'] = "BLINDED"

    oneprovider_configuration = oneprovider_client.configuration.Configuration()
    oneprovider_configuration.host = "https://BLINDED.muni.cz/api/v3/oneprovider"
    oneprovider_configuration.api_key['X-Auth-Token'] = "BLINDED"

    parameters: dict = request.json
    if {"name", "path", "support_size", "share_description"}.symmetric_difference(set(parameters.keys())):
        return "now enough or not allowed parameters"

    # create an instance of the API class
    api_instance = onezone_client.UserApi(onezone_client.ApiClient(onezone_configuration))
    body = onezone_client.SpaceCreateRequest(
        name=parameters["name"],
        # organization_name="Name of the organization got from local variable",
    )  # SpacesBody | Space creation data. (optional)

    api_response = None

    try:
        # Create new space
        api_response = api_instance.create_user_space(body=body)
        # api_response = api_instance.create_user_space(body=body, _preload_content=False)
    except ApiExceptionZone as e:
        print("Exception when calling SpaceApi->create_space: %s\n" % e)

    body, status_code, headers = api_response
    location = headers.get("location")
    space_id = location.split("/")[-1]

    api_instance = onepanel_client.StoragesApi(onepanel_client.ApiClient(onepanel_configuration))
    body = onepanel_client.StorageCreateRequest(
        {
            parameters["name"]: {
                "type": "posix",
                "mountPoint": parameters["path"],
                "importedStorage": True,
                "readonly": True
            }
        }
    )

    try:
        # Add storage
        api_response = api_instance.add_storage(body)
        pprint(api_response)
    except ApiExceptionPanel as e:
        print("Exception when calling StoragesApi->add_storage: %s\n" % e)

    storage_id = None
    for storage_name, storage_info in api_response.items():
        storage_id = storage_info["id"]

    api_instance = onezone_client.TokenApi(onezone_client.ApiClient(onezone_configuration))
    body = onezone_client.TemporaryTokenCreateRequest(
        type={"inviteToken": {"inviteType": "supportSpace", "spaceId": space_id}},
        caveats=[{"type": "time", "validUntil": int(time.time()) + 120}])

    try:
        # Create temporary token for current user
        api_response = api_instance.create_temporary_token_for_current_user(body)
        pprint(api_response)
    except ApiExceptionZone as e:
        print("Exception when calling TokenApi->create_temporary_token_for_current_user: %s\n" % e)

    invite_token = api_response.token

    api_instance = onepanel_client.SpaceSupportApi(onepanel_client.ApiClient(onepanel_configuration))
    body = onepanel_client.SpaceSupportRequest(
        token=invite_token,
        size=parameters["support_size"],
        storage_id=storage_id,
        storage_import=onepanel_client.StorageImport(
            mode="auto",
            auto_storage_import_config=onepanel_client.AutoStorageImportConfig(
                continuous_scan=True,
                scan_interval=60,
                detect_modifications=True,
                detect_deletions=True
            )),
    )

    try:
        # Support space
        api_response = api_instance.support_space(body)
        pprint(api_response)
    except ApiExceptionPanel as e:
        print("Exception when calling SpaceSupportApi->support_space: %s\n" % e)

    support_id = api_response.id

    api_instance = oneprovider_client.SpaceApi(oneprovider_client.ApiClient(oneprovider_configuration))

    for try_number in range(10):
        print("Getting space info try: %d/10" % (try_number + 1))
        time.sleep(1)
        try:
            # Get basic space information
            api_response = api_instance.get_space(space_id)
            pprint(api_response)
            break
        except ApiExceptionProvider as e:
            print("Exception when calling SpaceApi->get_space: %s\n" % e)

    file_id = api_response.file_id

    description = create_metadata_md(parameters["name"], "Masaryk University", file_id,
                                     os.path.join(parameters["path"] + "/SPA.yml"))

    api_instance = oneprovider_client.ShareApi(oneprovider_client.ApiClient(oneprovider_configuration))
    body = oneprovider_client.ShareCreateRequest(
        name=parameters["name"],
        description=description,
        root_file_id=file_id
    )

    try:
        # Create share
        api_response = api_instance.create_share(body)
        pprint(api_response)
    except ApiExceptionProvider as e:
        print("Exception when calling ShareApi->create_share: %s\n" % e)

    share_id = api_response.share_id

    api_instance = oneprovider_client.ShareApi(oneprovider_client.ApiClient(oneprovider_configuration))

    try:
        # Get share info
        api_response = api_instance.get_share(share_id)
        pprint(api_response)
    except ApiExceptionProvider as e:
        print("Exception when calling ShareApi->get_share: %s\n" % e)

    share_purl = api_response.public_url

    response = flask.Response(json.dumps({
        "status": status_code,
        "space_id": space_id,
        "space_file_id": file_id,
        "location": location,
        "storage_id": storage_id,
        "support_id": support_id,
        "public_share_url": share_purl
    }))
    response.headers["Content-Type"] = "application/json"
    return response



