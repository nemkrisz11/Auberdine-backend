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
                name=form.name,
                email=form.email,
                pwd_hash=ph.hash(form.password)
            ).save()
        except NotUniqueError:
            return False

        return True  # TODO: This is not what we agreed on in the API docs.

    else:
        return False
