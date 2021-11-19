from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from flaskapp.models.user import User
from bson.objectid import ObjectId, InvalidId


class FriendsApi(Resource):
    @jwt_required()
    def get(self):
        friends = []

        for friend_id in current_user.friends:
            friend = User.objects.get(id__exact=friend_id)
            friends.append({
                "name": str(friend.name),
                "user_id": str(friend.id)
            })

        return jsonify(friends)

    @jwt_required()
    def delete(self):
        if not request.is_json or "friend_id" not in request.json:
            return jsonify(deleted=False)

        try:
            oid = ObjectId(request.json["friend_id"])
            current_user.friends.remove(oid)
            current_user.save()
            return jsonify(deleted=True)
        except (ValueError, InvalidId):
            return jsonify(deleted=False)



