from flask import request, jsonify, Blueprint
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHash
from flask_jwt_extended import create_access_token

from flaskapp.routes.forms import LoginForm
from flaskapp.models.user import User

bp = Blueprint('login_api', __name__, url_prefix="/user")


@bp.route("/login", methods=['POST'])
def login_user():
    """
    Logs in a user
    e.g: POST /user/login
    """
    form = LoginForm(request.form)

    if form.validate():
        stored_user = User.objects(email=form.email.data).first()

        ph = PasswordHasher()

        try:
            ph.verify(stored_user.pwd_hash, form.password.data)

            # Generate token
            access_token = create_access_token(identity=form.email.data)

            return jsonify(access_token=access_token)

        except VerifyMismatchError:
            print(f"Authentication failed for user: {str(form.email.data)}. Caused by: Bad password")
            return "None"  # TODO

        except InvalidHash:
            print(f"Authentication failed for user: {str(form.email.data)}. Caused by: Invalid hash in db")
            return "None"  # TODO

        except VerificationError:
            print(f"Authentication failed for user: {str(form.email.data)}. Caused by: Unknown")
            return "None"  # TODO
