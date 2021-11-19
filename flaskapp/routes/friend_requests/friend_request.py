from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from flaskapp.models.user import User
from bson.objectid import ObjectId, InvalidId
from mongoengine.errors import DoesNotExist


class FriendRequestsApi(Resource):
    @jwt_required()
    def get(self):
        reqs = []

        for _id in current_user.friend_requests:
            candidate = User.objects.get(id__exact=_id)
            reqs.append({
                "name": candidate.name,
                "user_id": str(candidate.id)
            })

        return jsonify(reqs)

    @jwt_required()
    def post(self):
        if not request.is_json or any([i not in request.json for i in ["user_id", "accepted"]]):
            return jsonify(msg="Invalid data type, user_id, accepted fields are needed in JSON")
        try:
            uid = ObjectId(request.json["user_id"])
            other_user = User.objects.get(id__exact=uid)
            accepted = request.json["accepted"]
        except (InvalidId, DoesNotExist):
            return jsonify(msg="Invalid user_id provided")

        if uid not in current_user.friend_requests:
            return jsonify(msg="Friend request does not exist")

        current_user.friend_requests.remove(uid)
        if accepted:
            current_user.friends.append(uid)
            other_user.friends.append(current_user.id)
        other_user.save()
        current_user.save()

        return jsonify(msg="ok")


class FriendRequestApi(Resource):
    @jwt_required()
    def post(self):
        if not request.is_json or "user_id" not in request.json:
            return jsonify(msg="Invalid data type, user_id is neeeded in JSON")

        try:
            uid = ObjectId(request.json["user_id"])
            other_user = User.objects.get(id__exact=uid)
        except (InvalidId, DoesNotExist):
            return jsonify(msg="Invalid user_id")

        if uid not in current_user.friend_requests and current_user.id not in other_user.friend_requests:
            other_user.friend_requests.append(current_user.id)
            other_user.save()
            return jsonify(msg="ok")
        else:
            return jsonify(msg="Friend request already exists")
