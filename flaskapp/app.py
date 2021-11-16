import os
from flask import Flask, request, jsonify
from mongoengine import StringField, ListField, URLField, BinaryField, ObjectIdField, DateTimeField, GeoPointField, IntField
from mongoengine import Document, connect

application = Flask(__name__)
application.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ[
    'MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':' + os.environ['MONGODB_PORT'] + '/' + os.environ['MONGODB_DATABASE']

connect(host=application.config["MONGO_URI"])


class User(Document):
    name = StringField(required=True)
    pwd_hash = BinaryField(required=True)
    hash_salt = BinaryField(required=True)
    email = StringField(required=True)
    friends = ListField(ObjectIdField)
    friend_requests = ListField(ObjectIdField)
    meta = {
        "collection": "users"
    }


class Place(Document):
    google_place_id = StringField()
    last_sync = DateTimeField()
    name = StringField(required=True)
    address = StringField(required=True)
    location = GeoPointField()
    website = URLField()
    meta = {
        "collection": "places"
    }


class Review(Document):
    user_id = ObjectIdField(required=True)
    place_id = ObjectIdField(required=True)
    rating = IntField(required=True)
    text = StringField(required=True)
    meta = {
        "collection": "reviews"
    }


@application.route("/place/new")
def new_place():
    """Creates a new place

    e.g: GET /place/new?name=Restaurant1
    """

    place = Place(name=request.args.get("name"),
                  address=request.args.get("address"))
    place.save()
    return "Place saved"


@application.route("/debug_places")
def list_places():
    """List places.

    e.g: GET /debug_places """

    places = list(Place.objects)
    places = map(lambda x: "<li>" + x.name +
                 ", " + x.address + "</li>", places)
    return "<p>Places</p><ul> {} </ul>".format("\n".join(places))


@application.route('/')
def index():
    application.logger.info("GOT A REQUEST!")
    return jsonify(
        status=True,
        message='Welcome to the Auberdine Flask application!'
    )


if __name__ == "__main__":
    ENV_DEBUG = os.environ.get("APPLICATION_DEBUG", True)
    ENV_PORT = os.environ.get("APPLICATION_PORT", 5000)
    application.run(host='0.0.0.0', port=ENV_PORT, debug=ENV_DEBUG)
