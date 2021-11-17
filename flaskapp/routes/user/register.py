from flask import request, Blueprint
from argon2 import PasswordHasher
from mongoengine import NotUniqueError

from flaskapp.routes.forms import RegisterForm
from flaskapp.models.user import User

bp = Blueprint('register_api', __name__, url_prefix="/user")


@bp.route("/register", methods=['POST'])
def register_user():
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
                pwd_hash=ph.hash(form.password.data)
            ).save()
        except NotUniqueError:
            return str(form.errors.items()) + f"Form: {str(request.form)}"  # TODO

        return "Successful registration!"  # TODO: This is not what we agreed on in the API docs.

    else:
        return str(form.errors.items()) + f"Form: {str(request.form)}"  # TODO:
