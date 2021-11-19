from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt
from flaskapp.authorization import jwt_redis_blocklist, TOKEN_EXPIRES


class LogoutApi(Resource):
    @jwt_required()
    def delete(self):
        """
        Logs out a user
        e.g: DELETE /user/logout
        """
        jti = get_jwt()["jti"]
        jwt_redis_blocklist.set(jti, "", ex=TOKEN_EXPIRES)
        return jsonify(msg="ok")
