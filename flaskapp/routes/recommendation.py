from flask import Blueprint

bp = Blueprint("recommendation", __name__, url_prefix="")


@bp.route("/user/recommendations")
def fetch_recommendation():
    pass
