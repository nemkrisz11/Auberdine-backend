from flask import Blueprint

bp = Blueprint("friend_request", __name__, url_prefix="/user")


@bp.route("/friend_requests", methods=["GET"])
def fetch_friend_requests():
    return "Hello world"


@bp.route("/friend_request", methods=["POST"])
def send_friend_request():
    pass


@bp.route("/friend_requests", methods=["POST"])
def reply_to_friend_request():
    pass


@bp.route("/friend_req", methods=["GET"])
def shit():
    return "FDLKsadfgg"

