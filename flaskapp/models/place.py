from mongoengine import Document, StringField, DateTimeField, PointField, URLField, ListField, BinaryField, BooleanField
from flaskapp.models.review import Review


class Place(Document):
    google_place_id = StringField()
    last_sync = DateTimeField()
    name = StringField(required=True)
    address = StringField(required=True)
    location = PointField()  # Pointfield stores a dict: {"type": "Point", "coordinates": [x,y]}
    website = URLField()
    pictures = ListField(BinaryField())
    picture_refs = ListField(StringField())
    reviews_fetched = BooleanField()
    meta = {
        "collection": "places"
    }

    def rating(self):
        revs = Review.objects(place_id__exact=self.id)
        total = 0.0
        for rev in revs:
            total += rev.rating
        return total / len(revs)

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
