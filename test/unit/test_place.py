import pytest
import json
import datetime
from flask import request

from fixtures import client
from flaskapp.api_query import query_20_places
from flaskapp.models.place import Place


def test_debug_places(client):
    rv = client.get("/place/debug_places")
    data = rv.json["places"]
    good = ["Dayka Gábor utca 3" in place["address"] for place in data]
    assert (any(good))


# def test_api(client):
    # textre = query_20_places(api_key="AIzaSyDtlpG0YZrvbKJ2U2BAnEfCq0nY8Gi7zTk",
    #                          fields=["formatted_address", "name", "geometry", "photo",
    #                                  "url", "type"],
    #                          radius=3000,
    #                          latitude=47.4926825844774,
    #                          longitude=19.013803073248987,
    #                          place_type="food")

    # for info in result["results"]:
    #     place = Place(google_place_id=info.get("place_id", None),
    #                   location=[info["geometry"]["location"]["lat"], info["geometry"]["location"]["lng"]],
    #                   name=info.get("name", None),
    #                   pictures=[photo["photo_reference"] for photo in info.get("photos", [])],
    #                   last_sync=datetime.datetime.utcnow(),
    #                   address=info.get("vicinity", None),
    #                   website=info.get("url", None)
    #                   )
    #     place.save()




