from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flaskapp.models.user import User
from flaskapp.models.place import Place
from flaskapp.models.review import Review
from bson.objectid import ObjectId, InvalidId
from mongoengine.errors import DoesNotExist
from flaskapp.assets.defaults import default_img
import base64



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

        ret_val = {
            "name": place.name,
            "address": place.address,
            "location": place.location["coordinates"],
            "rating": place.rating(),
            "reviews": reviews,
        }

        if place.website:
            ret_val["website"] = place.website

        if len(place.pictures) > 0:
            ret_val["picture"] = base64.b64encode(place.pictures[0]).decode("UTF-8")
        else:
            ret_val["picture"] = default_img

        return jsonify(ret_val)


