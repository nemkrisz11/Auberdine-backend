from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required


class IndexApi(Resource):
    @jwt_required()
    def get(self):
        return jsonify(
            status=True,
            message='Welcome to the Auberdine Flask application!'
        )
