from __future__ import print_function

import json
from typing import TypedDict

import flask
from flask import Blueprint, request
import onezone_client
from onezone_client.rest import ApiException
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
    configuration = onezone_client.configuration.Configuration()
    configuration.host = "https://BLINDED.muni.cz/api/v3/onezone"
    configuration.api_key['X-Auth-Token'] = "BLINDED"

    parameters: dict = request.json
    if {"name"}.symmetric_difference(set(parameters.keys())):
        return "now allowed parameters"

    # create an instance of the API class
    api_instance = onezone_client.UserApi(onezone_client.ApiClient(configuration))
    body = onezone_client.SpaceCreateRequest(
        name=parameters["name"],
        # organization_name="Name of the organization got from local variable",
    )  # SpacesBody | Space creation data. (optional)

    try:
        # Create new space
        api_response = api_instance.create_user_space(body=body)
    except ApiException as e:
        print("Exception when calling SpaceApi->create_space: %s\n" % e)

    body, status_code, headers = api_response

    response = flask.Response(json.dumps({
        "status": status_code,
        "body": body,
        "location": headers.get("location")
    }))
    response.headers["Content-Type"] = "application/json"
    return response



