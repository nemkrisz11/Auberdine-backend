from mongoengine import Document, StringField, DateTimeField, PointField, URLField, ListField


class Place(Document):
    google_place_id = StringField()
    last_sync = DateTimeField()
    name = StringField(required=True)
    address = StringField(required=True)
    location = PointField()
    website = URLField()
    pictures = ListField(StringField())
    meta = {
        "collection": "places"
    }

    def __repr__(self):
        fields = {
            "google_place_id": self.google_place_id,
            "last_sync": self.last_sync,
            "name": self.name,
            "address": self.address,
            "location": self.location,
            "website": self.website,
            "pictures": self.pictures
        }
        return "Place(" + repr(fields) + ")"

    def __str__(self):
        return repr(self)