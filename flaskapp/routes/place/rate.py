from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from flaskapp.models.user import User
from flaskapp.models.place import Place
from flaskapp.models.review import Review
from bson.objectid import ObjectId, InvalidId
from mongoengine.errors import DoesNotExist


class RatePlaceApi(Resource):
    @jwt_required()
    def post(self):
        if not request.is_json or any([i not in request.json for i in ["place_id", "rating", "description"]]):
            return jsonify(msg="Invalid data type: [place_id, rating, description] fields are needed in JSON")

        try:
            pid = ObjectId(str(request.json["place_id"]))
            place = Place.objects.get(id__exact=pid)
        except (InvalidId, DoesNotExist):
            return jsonify(msg="Invalid place_id provided")

        try:
            rating = int(request.json["rating"])
            desc = str(request.json["description"])
        except ValueError:
            return jsonify(msg="Invalid rating provided")

        existing_review = Review.objects(place_id__exact=pid, user_id__exact=current_user.id)
        if len(existing_review) > 0:
            existing_review[0].delete()

        review = Review(user_id=current_user.id, place_id=pid, rating=rating, text=desc)
        review.save()
        return jsonify(msg="ok")
