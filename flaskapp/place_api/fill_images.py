from flaskapp import app
from flaskapp.models.place import Place
from flaskapp.place_api.api_query import *
import time
import json
import datetime
import random


def query_photo_for_place(place, api_key):
    print("Retrieving image for: {}, {}".format(place.name, place.google_place_id))
    ref = place.picture_refs[0]
    photo_binary = query_photo(api_key, ref)
    if photo_binary is None:
        print("error in query")
        return

    print("Image binary starts with: {}".format(photo_binary[:5]))
    place.pictures.append(photo_binary)
    place.save()



if __name__ == "__main__":
    client = app.create_app()
    TIME_DELAY = 1.3
    N_QUERIES = 500
    api_key = "AIzaSyDtlpG0YZrvbKJ2U2BAnEfCq0nY8Gi7zTk"


    q = 0
    places = Place.objects
    for pl in places:
        if pl.pictures == [] and pl.picture_refs:
            query_photo_for_place(pl, api_key=api_key)
            q += 1
            if q >= N_QUERIES:
                break
            time.sleep(TIME_DELAY)

