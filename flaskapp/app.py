import os
from flask import Flask, request, jsonify
#from mongoengine import StringField, Document, connect

application = Flask(__name__)
application.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ[
    'MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':' + os.environ['MONGODB_PORT'] + '/' + os.environ['MONGODB_DATABASE']

# connect(host=application.config["MONGO_URI"])


# class User(Document):
#     name = StringField(required=True)
#     email = StringField()


# class Place(Document):
#     name = StringField(required=True)
#     address = StringField(required=True)


# @application.route("/place/new")
# def new_place():
#     """Creates a new place

#     e.g: GET /place/new?name=Restaurant1
#     """

#     place = Place(name=request.args.get("name"),
#                   address=request.args.get("address"))
#     place.save()
#     print(place.name, place.address)
#     return "Place saved"


# @application.route("/places")
# def list_places():
#     """List places.

#     e.g: GET /places """

#     places = list(Place.objects)
#     places = map(lambda x: "<li>" + x.name +
#                  ", " + x.address + "</li>", places)
#     return "<p>Places</p><ul> {} </ul>".format("\n".join(places))


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
