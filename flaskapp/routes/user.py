from flask import Blueprint

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/register", methods=["POST"])
def register():
    pass


@bp.route("/login", methods=["POST"])
def login():
    pass


