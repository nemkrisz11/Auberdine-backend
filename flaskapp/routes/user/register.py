from flask import request
from flask_restful import Resource
from argon2 import PasswordHasher
from mongoengine import NotUniqueError

from flaskapp.routes.forms import RegisterForm
from flaskapp.models.user import User


class RegisterApi(Resource):
    def post(self):
        """
        Creates a new user
        e.g: POST /user/register
        """
        form = RegisterForm(request.form)

        return_data = {i: True for i in ["namevalid", "emailvalid", "passwordvalid"]}

        if form.validate():
            ph = PasswordHasher()

            try:
                new_user = User(
                    name=form.name.data,
                    email=form.email.data,
                    password=ph.hash(form.password.data)
                ).save()
            except NotUniqueError:
                return_data["emailvaild"] = False

        else:
            errors = form.errors.keys()
            if "email" in errors:
                return_data["emailvalid"] = False
            if "name" in errors:
                return_data["namevalid"] = False
            if "password" in errors or "confirm" in errors:
                return_data["passwordvalid"] = False

        return return_data