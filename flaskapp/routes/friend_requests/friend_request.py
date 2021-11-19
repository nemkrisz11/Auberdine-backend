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
            return jsonify(success=False)

        try:
            uid = ObjectId(request.json["user_id"])
            other_user = User.objects.get(id__exact=uid)
            accepted = request.json["accepted"]
        except (InvalidId, DoesNotExist):
            return jsonify(success=False)

        if uid not in current_user.friend_requests:
            return jsonify(success=False)

        current_user.friend_requests.remove(uid)
        if accepted:
            current_user.friends.append(uid)
            other_user.friends.append(current_user.id)
        other_user.save()
        current_user.save()

        return jsonify(success=True)


class FriendRequestApi(Resource):
    @jwt_required()
    def post(self):
        if not request.is_json or "user_id" not in request.json:
            return jsonify(success=False)

        try:
            uid = ObjectId(request.json["user_id"])
            other_user = User.objects.get(id__exact=uid)
        except (InvalidId, DoesNotExist):
            return jsonify(success=False)

        if uid not in current_user.friend_requests and current_user.id not in other_user.friend_requests:
            other_user.friend_requests.append(current_user.id)
            other_user.save()
            return jsonify(success=True)
        else:
            return jsonify(success=False)
