from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from flaskapp.models.user import User
from flaskapp.models.place import Place
from flaskapp.models.review import Review
from bson.objectid import ObjectId, InvalidId
from mongoengine.errors import DoesNotExist


class GetPlaceApi(Resource):
    @jwt_required()
    def get(self, place_id):
        try:
            pid = ObjectId(str(place_id))
            place = Place.objects.get(id__exact=pid)
        except (InvalidId, DoesNotExist):
            return jsonify(msg="Place does not exist")

        revs = Review.objects(place_id__exact=pid)[:20]
        reviews = []
        for rev in revs:
            user = User.objects.get(id__exact=rev.user_id)
            reviews.append({
                "user_id": str(rev.user_id),
                "rating": rev.rating,
                "name": user.name,
                "description": rev.text
            })

        return jsonify({
            "name": place.name,
            "address": place.address,
            "website": str(place.website),
            "location": place.location["coordinates"],
            "rating": place.rating(),
            "reviews": reviews
        })


