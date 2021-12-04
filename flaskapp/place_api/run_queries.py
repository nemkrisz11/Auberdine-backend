from flaskapp import app
from flaskapp.models.place import Place
from flaskapp.place_api.api_query import *
import time
import json
import datetime
import random


# about the center: 47.497343752384765, 19.058862778883373
MIN_LAT = 47.443785576830216
MAX_LAT = 47.54632382139647
MIN_LONG = 18.97140571531646
MAX_LONG = 19.179112897227625
lat_mu = (MIN_LAT + MAX_LAT) / 2
long_mu = (MIN_LONG + MAX_LONG) / 2
lat_std = (MAX_LAT - MIN_LAT) / 4
long_std = (MAX_LONG - MIN_LONG) / 4


def get_random_budapest_circle(radius="random"):
    """Returns a tuple containing coordinates of a circle in Budapest

    Returns
    -------
    tuple: (latitude, longitude, radius)
    """

    latitude = random.gauss(lat_mu, lat_std)
    longitude = random.gauss(long_mu, long_std)
    if radius == "random":
        radius = round(random.uniform(700, 2000))
    return (latitude, longitude, radius)


if __name__ == "__main__":
    client = app.create_app()
    N_QUERIES = 100
    TIME_DELAY = 10.0
    api_key = "AIzaSyDtlpG0YZrvbKJ2U2BAnEfCq0nY8Gi7zTk"
    fields = ["formatted_address", "name", "geometry", "url"]

    q = 0
    next_page_token = None
    while q < N_QUERIES:
        if next_page_token:
            res = query_by_pagetoken(api_key, next_page_token)
        else:
            latitude, longitude, radius = get_random_budapest_circle()
            res = query_20_places(api_key, latitude, longitude, radius, fields)
        q += 1

        print("======= Query {} ========".format(q))
        if next_page_token is None:
            print("Location: ({}, {}, {})".format(round(latitude,5), round(longitude,5), radius))
        else:
            print("querying by pagetoken")

        if "next_page_token" in res:
            next_page_token = res["next_page_token"]
        else:
            next_page_token = None

        for pl in res["results"]:
            google_id = pl["place_id"]
            objs = Place.objects(google_place_id__exact=google_id)
            if len(objs) > 0:
                continue

            new_pl = Place(google_place_id=google_id,
                           last_sync=datetime.datetime.now(),
                           name=pl["name"],
                           address=pl.get("vicinity", ""),
                           location=[pl["geometry"]["location"]["lat"], pl["geometry"]["location"]["lng"]])

            url = pl.get("website", pl.get("url", None))
            if url:
                new_pl.website = url

            photo_refs = []
            for photo in pl.get("photos", []):
                photo_refs.append(photo["photo_reference"])
            if photo_refs:
                new_pl.picture_refs = photo_refs

            new_pl.save()
            print("Place saved: {}".format(new_pl.name))


        # wait until the next query
        time.sleep(TIME_DELAY)




