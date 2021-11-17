from flask import Blueprint, request
from models.place import Place

bp = Blueprint("place", __name__, url_prefix="/place")


@bp.route("/new")
def DEBUG_create_place():
    """Creates a new place

    e.g: GET /place/new?name=Restaurant1
    """

    place = Place(name=request.args.get("name"),
                  address=request.args.get("address"))
    place.save()
    return "Place saved"


@bp.route("/debug_places")
def DEBUG_list_places():
    """List places.

    e.g: GET /debug_places """

    places = list(Place.objects)
    places = map(lambda x: "<li>" + x.name +
                 ", " + x.address + "</li>", places)
    return "<p>Places</p><ul> {} </ul>".format("\n".join(places))