from flask import request
import pytest
from fixtures import client, token
from flaskapp.models.user import User
from bson.objectid import ObjectId, InvalidId


@pytest.mark.email("pista1@x.y")
@pytest.mark.password("kutyafasz")
def test_get_friends(client, token):
    resp = client.get("/user/friends", headers={"Authorization": "Bearer " + token})
    assert resp.status_code == 200
    assert resp.headers["Content-Type"] == "application/json"
    assert len(resp.json) == 2
    for user in resp.json:
        assert "user_id" in user
        assert "name" in user
        uid = ObjectId(user["user_id"])
        name = user["name"]
        assert (name in ["Dr. Goldschmidt Balázs", "Pista2"])

        user_by_uid = User.objects(id__exact=uid)
        assert len(user_by_uid) == 1
        assert user_by_uid[0].name == name


@pytest.mark.email("pista1@x.y")
@pytest.mark.password("kutyafasz")
def test_delete_friend(client, token):
    friend2 = User.objects.get(email__exact="goldschmidt@iit.bme.hu")
    resp = client.delete("/user/friends", json={"friend_id": str(friend2.id)},
                         headers={"Authorization": "Bearer " + token})
    assert resp.status_code == 200
    assert resp.headers["Content-Type"] == "application/json"
    assert resp.json["msg"] == "ok"
    user = User.objects.get(email__exact="pista1@x.y")
    assert len(user.friends) == 1
    friend2 = User.objects.get(email__exact="goldschmidt@iit.bme.hu")
    assert len(friend2.friends) == 0


@pytest.mark.email("vlad@kreml.ru")
@pytest.mark.password("12345678")
def test_delete_friend_error(client, token):
    non_friend = User.objects.get(email__exact="goldschmidt@iit.bme.hu")
    resp = client.delete("/user/friends", json={"friend_id": str(non_friend.id)},
                         headers={"Authorization": "Bearer " + token})
    assert resp.status_code == 200
    assert resp.headers["Content-Type"] == "application/json"
    assert not resp.data.decode("UTF-8") == '"ok"\n'
    user = User.objects.get(email__exact="vlad@kreml.ru")
    assert len(user.friends) == 0


@pytest.mark.email("neumann@x.z")
@pytest.mark.password("12345678")
def test_get_friend_requests(client, token):
    resp = client.get("/user/friend_requests", headers={"Authorization": "Bearer " + token})
    assert resp.status_code == 200 and resp.is_json
    assert len(resp.json) == 2
    for user in resp.json:
        assert "user_id" in user and "name" in user
        uid = ObjectId(user["user_id"])
        us = User.objects.get(id__exact=uid)
        assert user["name"] == us.name


@pytest.mark.email("neumann@x.z")
@pytest.mark.password("12345678")
def test_accept_friend_req(client, token):
    other = User.objects.get(email__exact="pista1@x.y")
    resp = client.post("/user/friend_requests", json={"user_id": str(other.id),
                                                      "accepted": True},
                       headers={"Authorization": "Bearer " + token})
    assert resp.status_code == 200 and resp.is_json
    assert resp.json["msg"] == "ok"
    other = User.objects.get(email__exact="pista1@x.y")
    user = User.objects.get(email__exact="neumann@x.z")
    assert user.id in other.friends
    assert other.id in user.friends
    assert other.id not in user.friend_requests


@pytest.mark.email("neumann@x.z")
@pytest.mark.password("12345678")
def test_decline_friend_req(client, token):
    other = User.objects.get(email__exact="pista1@x.y")
    resp = client.post("/user/friend_requests", json={"user_id": str(other.id),
                                                      "accepted": False},
                       headers={"Authorization": "Bearer " + token})
    assert resp.status_code == 200 and resp.is_json
    assert resp.json["msg"] == "ok"
    other = User.objects.get(email__exact="pista1@x.y")
    user = User.objects.get(email__exact="neumann@x.z")
    assert user.id not in other.friends
    assert other.id not in user.friends
    assert other.id not in user.friend_requests


@pytest.mark.email("neumann@x.z")
@pytest.mark.password("12345678")
def test_send_friend_req(client, token):
    other = User.objects.get(email__exact="vlad@kreml.ru")
    resp = client.post("/user/friend_request", json={"user_id": str(other.id)},
                       headers={"Authorization": "Bearer " + token})
    assert resp.status_code == 200 and resp.is_json
    assert resp.json["msg"] == "ok"
    other = User.objects.get(email__exact="vlad@kreml.ru")
    user = User.objects.get(email__exact="neumann@x.z")
    assert user.id in other.friend_requests
    assert user.id not in other.friends
    assert other.id not in user.friend_requests
    assert other.id not in user.friends


@pytest.mark.email("neumann@x.z")
@pytest.mark.password("12345678")
def get_user_search(client, token):
    pass