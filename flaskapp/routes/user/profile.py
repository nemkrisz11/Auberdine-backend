from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required

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
        user = User.objects.get(id=user_id)
        user_reviews = Review.objects(user_id=user_id)

        user_reviewed_places = []
        for review in user_reviews:
            place = Place.objects.get(id=review.place_id)
            user_reviewed_places.append({
                "place_id": str(review.place_id),
                "place_name": place.name,
                "address": place.address,
                "rating": review.rating,
                "text": review.text,
                # "friend_ratings": []
            })

        return jsonify({
            "name": user.name,
            "reviews": user_reviewed_places
        })
