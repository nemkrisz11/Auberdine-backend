from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from flaskapp.models.user import User
from bson.objectid import ObjectId, InvalidId
from mongoengine.errors import DoesNotExist


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
            return jsonify(msg="Invalid data type, friend_id is required in JSON")

        try:
            oid = ObjectId(str(request.json["friend_id"]))
            current_user.friends.remove(oid)
            current_user.save()
            other_user = User.objects.get(id__exact=oid)
            other_user.friends.remove(current_user.id)
            other_user.save()
            return jsonify(msg="ok")
        except (ValueError, InvalidId, DoesNotExist):
            return jsonify(msg="Invalid friend_id")



