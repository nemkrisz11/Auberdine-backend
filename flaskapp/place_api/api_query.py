import json
import requests
from urllib import parse


def query_20_places(api_key, latitude, longitude, radius, fields, language="hu", place_type="food"):
    params = {
        "location": "{},{}".format(latitude, longitude),
        "radius": str(radius),
        "fields": ",".join(fields),
        "type": place_type,
        "language": language,
        "key": api_key
    }

    items = list(params.items())
    querystring = parse.urlencode(items)
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?" + querystring
    response = requests.request("GET", url)
    return response.text


def query_by_pagetoken(api_key, token):
    params = {
        "key": api_key,
        "pagetoken": str(token)
    }
    items = list(params.items())
    querystring = parse.urlencode(items)
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?" + querystring
    response = requests.request("GET", url)
    return response.text


def query_photo(api_key, photo_ref, width=800, height=800):
    params = {
        "maxwidth": str(width),
        "maxheight": str(height),
        "key": api_key,
        "photo_reference": photo_ref
    }
    items = list(params.items())
    querystring = parse.urlencode(items)
    url = "https://maps.googleapis.com/maps/api/place/photo?" + querystring
    response = requests.request("GET", url)
    return response.content


