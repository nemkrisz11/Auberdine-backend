from mongoengine import Document, ObjectIdField, IntField, StringField


class Review(Document):
    user_id = ObjectIdField(required=True)
    place_id = ObjectIdField(required=True)
    rating = IntField(required=True)
    text = StringField(required=True)
    meta = {
        "collection": "reviews"
    }

    def __repr__(self):
        fields = {
            "user_id": self.user_id,
            "place_id": self.place_id,
            "rating": self.rating,
            "text": self.text
        }
        return repr(fields)

    def __str__(self):
        return repr(self)