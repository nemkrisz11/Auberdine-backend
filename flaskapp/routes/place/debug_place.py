from flask import Response, jsonify
from flaskapp.models.place import Place
from flask_restful import Resource


class DebugPlaceApi(Resource):
    def get(self):
        places = list(Place.objects)
        places = [{"name": x.name, "address": x.address} for x in places]
        places = {
            "places": places
        }
        return jsonify(places)