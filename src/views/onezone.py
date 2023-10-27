from __future__ import print_function

import json

import flask
from flask import Blueprint
import onezone_client
from onezone_client.rest import ApiException
from pprint import pprint

onezone_bp = Blueprint('onezone', __name__, url_prefix='/onezone', static_folder="../static")


@onezone_bp.route("/", methods=["GET"])
def get():
    configuration = onezone_client.configuration.Configuration()
    configuration.host = "https://BLINDED.muni.cz/api/v3/onezone"
    configuration.api_key['X-Auth-Token'] = "BLINDED"

    # create an instance of the API class
    api_instance = onezone_client.SpaceApi(onezone_client.ApiClient(configuration))

    try:
        # List all spaces
        api_response = api_instance.list_spaces()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SpaceApi->list_spaces: %s\n" % e)

    response = flask.Response(json.dumps(api_response.to_dict()))
    response.headers["Content-Type"] = "application/json"
    return response


@onezone_bp.route("/", methods=["POST"])
def post():
    return "Return from example POST"
