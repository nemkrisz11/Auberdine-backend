from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from bson.objectid import ObjectId, InvalidId
from mongoengine.errors import DoesNotExist

from flaskapp.models.user import User
from flaskapp.models.review import Review
from flaskapp.models.place import Place


class ProfileApi(Resource):
    @jwt_required()
    def get(self, user_id):
        """
        Fetches the user profile
        e.g: GET /user/<user_id>
        """

        try:
            uid = ObjectId(str(user_id))
            user = User.objects.get(id__exact=uid)
        except (InvalidId, DoesNotExist):
            return jsonify({"msg": "User does not exist"})

        # get always the first 20 reviews, paging on the frontend could fix this
        user_reviews = Review.objects(user_id=str(user_id))[:20]

        user_reviewed_places = []
        for review in user_reviews:
            place_reviews = Review.objects(place_id=review.place_id)
            friend_ratings = []
            for rev in place_reviews:
                if rev.user_id not in current_user.friends:
                    continue
                friend = User.objects.get(id=str(rev.user_id))
                friend_ratings.append({
                    "rating": rev.rating,
                    "name": friend.name
                })

            place = Place.objects.get(id=review.place_id)
            user_reviewed_places.append({
                "place_id": str(review.place_id),
                "place_name": place.name,
                "rating": place.rating(),
                "friend_ratings": friend_ratings
            })

        return jsonify({
            "name": user.name,
            "reviews": user_reviewed_places
        })
