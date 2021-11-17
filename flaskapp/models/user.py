from mongoengine import Document, StringField, ListField, BinaryField, ObjectIdField


class User(Document):
    name = StringField(required=True)
    pwd_hash = BinaryField(required=True)
    # hash_salt = BinaryField(required=True)
    email = StringField(required=True)
    friends = ListField(ObjectIdField)
    friend_requests = ListField(ObjectIdField)
    meta = {
        "collection": "users"
    }

    def __repr__(self):
        fields = {
            "name": self.name,
            "pwd_hash": self.pwd_hash,
            "email": self.email,
            "friends": self.friends,
            "friend_requests": self.friend_requests
        }