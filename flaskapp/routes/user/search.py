from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from flaskapp.models.user import User


class UserSearchApi(Resource):
    """Search for users with matching names.
    Queries are OR queries on exact word matches currently.
    """

    @jwt_required()
    def post(self):
        if not request.is_json or "query" not in request.json:
            return jsonify(users=[], msg="Invalid request, query key needed in JSON")

        query = str(request.json["query"])
        result = User.objects.search_text(query).order_by("$text_score")

        results = []
        for user in result:
            results.append({
                "name": user.name,
                "user_id": str(user.id)
            })

        return jsonify(users=results)
