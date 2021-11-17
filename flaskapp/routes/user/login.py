from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token

from flaskapp.routes.forms import LoginForm
from flaskapp.models.user import User


class LoginApi(Resource):
    def post(self):
        """
        Logs in a user
        e.g: POST /user/login
        """
        form = LoginForm(request.form)

        if form.validate():
            stored_user = User.objects.get(email=form.email.data)

            if stored_user.check_password(form.password.data):
                access_token = create_access_token(identity=form.email.data)
                return jsonify(access_token=access_token)
