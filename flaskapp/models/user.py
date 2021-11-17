from mongoengine import Document, StringField, ListField, ObjectIdField
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHash


class User(Document):
    name = StringField(required=True)
    password = StringField(required=True)
    email = StringField(required=True, unique=True)
    friends = ListField(ObjectIdField)
    friend_requests = ListField(ObjectIdField)
    meta = {
        "collection": "users"
    }

    def check_password(self, password):
        try:
            ph = PasswordHasher()
            return ph.verify(self.password, password)
        except (VerifyMismatchError, VerificationError, InvalidHash):
            return False

    def __repr__(self):
        fields = {
            "name": self.name,
            "password": self.password,
            "email": self.email,
            "friends": self.friends,
            "friend_requests": self.friend_requests
        }