from flask import request, jsonify, Blueprint
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHash
from flask_jwt_extended import create_access_token

from flaskapp.routes.forms import LoginForm
from flaskapp.models.user import User

bp = Blueprint('login_api', __name__, url_prefix="/user")


@bp.route("/login", methods=['POST'])
def login_user():
    form = LoginForm(request.form)

    if form.validate():
        stored_user = User.objects(email=form.email)[0]

        ph = PasswordHasher()

        try:
            ph.verify(stored_user.pwd_hash, form.password)

            # Generate token
            access_token = create_access_token(identity=form.email)

            return jsonify(access_token=access_token)

        except VerifyMismatchError:
            print(f"Authentication failed for user: {form.email}. Caused by: Bad password")
            return None

        except InvalidHash:
            print(f"Authentication failed for user: {form.email}. Caused by: Invalid hash in db")
            return None

        except VerificationError:
            print(f"Authentication failed for user: {form.email}. Caused by: Unknown")
            return None
