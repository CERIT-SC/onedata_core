from flask import Blueprint

example_bp = Blueprint('example', __name__, url_prefix='/example', static_folder="../static")


@example_bp.route("/", methods=["GET"])
def get():
    return "Return from example GET"


@example_bp.route("/", methods=["POST"])
def post():
    return "Return from example POST"
