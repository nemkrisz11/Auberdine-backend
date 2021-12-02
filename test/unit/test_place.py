import pytest
import json
import datetime
from flask import request

from fixtures import client, token
from flaskapp.api_query import query_20_places
from flaskapp.models.place import Place
from flaskapp.models.review import Review
from flaskapp.models.user import User


@pytest.mark.email("newton@gravity.org")
@pytest.mark.password("12345678")
def test_get_place(client, token):
    place = Place.objects.get(name__exact="Burger King")
    headers = {"Authorization": "Bearer " + token}
    resp = client.get("/api/place/{}".format(place.id), headers=headers)
    assert resp.is_json and resp.status_code == 200
    val = resp.json
    assert val["name"] == "Burger King"
    assert val["address"] == "Budapest, Széna tér 7"
    print(val["location"])
    assert type(val["location"]) == list
    assert val["rating"] == 2.0

    assert "reviews" in val
    assert len(val["reviews"]) == 2
    for rev in val["reviews"]:
        assert rev["name"] in ("Vladimir Putin", "Isaac Newton")


@pytest.mark.email("newton@gravity.org")
@pytest.mark.password("12345678")
def test_rate_place(client, token):
    headers = {"Authorization": "Bearer " + token}
    place = Place.objects.get(name__exact="Larus Étterem")
    user = User.objects.get(email__exact="newton@gravity.org")
    data = {
        "place_id": str(place.id),
        "rating": 4,
        "description": "This is a new review."
    }
    resp = client.post("/api/place/rate", json=data, headers=headers)
    assert resp.is_json and resp.status_code == 200
    assert resp.json == {} or resp.json["msg"] == "ok"
    review = Review.objects.get(place_id__exact=place.id, user_id__exact=user.id)
    assert review.rating == 4
    assert review.text == "This is a new review."



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
