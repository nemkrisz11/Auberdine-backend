import pytest
from fixtures import client, token
from flaskapp.models.user import User


def test_get_user():
    """Test for GET /user/{user_id} route

    """

    users = User.objects(name__contains="Goldschmidt")
    assert len(users) == 1
    user = users[0]
    assert "iit" in user.email

    users = User.objects()
    assert len(users) >= 6
    #client.get("/user/{}".format(user._id))


def test_valid_register(client):
    resp = client.post("/user/register",
                data={"name": "thisisauniqueuser34958",
                      "password": "12345678",
                      "confirm": "12345678",
                      "email": "uniqueemail53498@a.b"
                      })

    assert resp.status_code == 200
    assert resp.is_json
    assert resp.json == {}


def test_invalid_register(client):
    data = {
        "name": "thisisauniqueuser34958",
        "password": "12345678",
        "confirm": "1234567",
        "email": "uniqueemail53498@a.b"
    }

    resp = client.post("/user/register", json=data)
    assert resp.status_code == 200 and resp.is_json
    assert "password" in resp.json

    data["email"] = "newton@gravity.org"
    resp = client.post("/user/register", json=data)
    assert "email" in resp.json and "password" in resp.json

    data["password"] = "1234567"
    resp = client.post("/user/register", json=data)
    assert "email" in resp.json and "password" in resp.json


def test_valid_login(client):
    resp = client.post("/user/login",
                       data={"email": "goldschmidt@iit.bme.hu",
                             "password": "12345678"})
    assert resp.status_code == 200
    assert resp.is_json and "access_token" in resp.json
    assert len(resp.json["access_token"]) > 20  # TODO: more sensible token check


def test_invalid_login(client):
    resp = client.post("/user/login",
                       data={"email": "goldschmidt@iit.bme.hu",
                             "password": "qwertyasd"})
    assert resp.status_code == 200
    assert resp.is_json
    assert "email" not in resp.json
    assert "password" in resp.json


@pytest.mark.email("newton@gravity.org")
@pytest.mark.password("12345678")
def test_logout(client, token):
    resp = client.delete("/user/logout", headers={"Authorization": "Bearer " + token})
    assert resp.status_code == 200 and resp.is_json
    assert resp.json["msg"] == "ok"

    resp = client.delete("/user/logout", headers={"Authorization": "Bearer " + token})
    assert resp.status_code == 401 and resp.is_json


@pytest.mark.email("newton@gravity.org")
@pytest.mark.password("12345678")
def test_search_valid(client, token):
    headers = {"Authorization": "Bearer " + token}
    search = lambda q: client.post("/user/search", json={"query": q}, headers=headers)

    query = "goldschmidt"
    resp = search(query)
    assert resp.is_json and "users" in resp.json
    print(resp.json)
    assert len(resp.json["users"]) == 1
    assert query in resp.json["users"][0]["name"].lower()

    query = "newton pista1"
    resp = search(query)
    assert resp.is_json and "users" in resp.json
    assert len(resp.json["users"]) == 2
    assert ["newton" in u or "pista" in u["name"].lower() for u in resp.json["users"]]

    query = "dostoevsky"
    resp = search(query)
    assert resp.is_json and "users" in resp.json
    assert len(resp.json["users"]) == 0


@pytest.mark.email("newton@gravity.org")
@pytest.mark.password("12345678")
def test_search_invalid(client, token):
    headers = {"Authorization": "Bearer " + token}
    resp = client.post("/user/search", json={"wrong_key": 5345}, headers=headers)
    assert resp.is_json
    assert bool(resp.json["msg"])
    assert len(resp.json["users"]) == 0


@pytest.mark.email("newton@gravity.org")
@pytest.mark.password("12345678")
def test_get_user_properties(client, token):
    headers = {"Authorization": "Bearer " + token}
    resp = client.get("/user/properties", headers=headers)
    assert resp.is_json and resp.status_code == 200
    assert resp.json["name"] == "Isaac Newton"
    assert resp.json["email"] == "newton@gravity.org"


@pytest.mark.email("newton@gravity.org")
@pytest.mark.password("12345678")
def test_set_user_properties_good_password(client, token):
    headers = {"Authorization": "Bearer " + token}
    resp = client.post("/user/properties", json={"password": "newton1234"}, headers=headers)
    assert resp.is_json and resp.status_code == 200
    assert "name" not in resp.json
    assert "password" not in resp.json


@pytest.mark.email("newton@gravity.org")
@pytest.mark.password("12345678")
def test_set_user_properties_bad_name_bad_pw(client, token):
    headers = {"Authorization": "Bearer " + token}
    resp = client.post("/user/properties", json={"name": "q", "password": "111234"}, headers=headers)
    assert resp.is_json and resp.status_code == 200
    assert "name" in resp.json
    assert "password" in resp.json
