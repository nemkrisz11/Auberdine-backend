from flask import request, jsonify
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

        if form.validate():
            ph = PasswordHasher()
            try:
                new_user = User(
                    name=form.name.data,
                    email=form.email.data,
                    password=ph.hash(form.password.data)
                ).save()
                return jsonify()
            except NotUniqueError:
                return jsonify(email=['Már létezik egy felhasználó ezzel az email címmel!'])
        else:
            return jsonify(form.errors)
