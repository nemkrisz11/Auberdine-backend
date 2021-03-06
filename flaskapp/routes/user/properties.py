from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from flaskapp.routes.forms import PropertiesForm


class PropertiesApi(Resource):
    @jwt_required()
    def get(self):
        """
        Request user properties
        e.g: GET /user/properties
        """
        return jsonify(
            id=str(current_user.id),
            name=str(current_user.name),
            email=str(current_user.email),
        )

    @jwt_required()
    def post(self):
        """
        Changes user properties
        e.g: POST /user/properties
        """
        form = PropertiesForm(request.form)

        if form.validate():
            if current_user.check_password(form.password.data):
                # Name change
                if form.new_name is not None:
                    current_user.name = form.new_name.data

                # Password change
                if form.new_password is not None:
                    current_user.change_password(form.new_password.data)

                current_user.save()
                return jsonify()
            else:
                return jsonify(password=['Helytelen jelszó!'])
        else:
            return jsonify(form.errors)
