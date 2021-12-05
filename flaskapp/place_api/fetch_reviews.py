from flaskapp import app
from flaskapp.models.place import Place
from flaskapp.models.user import User
from flaskapp.models.review import Review
from flaskapp.place_api.api_query import *
import time
import json
import datetime
import random
from argon2 import PasswordHasher


def next_char(choice=None):
    if choice is None:
        choice = random.randint(0, 2)
    if choice == 0:
        return chr(random.randint(ord('0'), ord('9')))
    if choice == 1:
        return chr(random.randint(ord('a'), ord('z')))
    return chr(random.randint(ord('A'), ord('Z')))


def gen_random_pw(length=20):
    pw = "".join([next_char() for i in range(length)])
    return pw


def gen_random_email():
    chars = [next_char(1)] + [next_char() for i in range(11)] + list("@example.com")
    return "".join(chars)


def query_reviews_for_place(place, api_key):
    print("Retrieving reviews for: {}".format(place.name))
    res = query_place_details(api_key, place.google_place_id, ["reviews"])
    if res is None:
        print("\tError in query.")
        return
    if "result" not in res or "reviews" not in res["result"]:
        print("\tNo reviews.")
        return
    print("\t{} reviews.".format(len(res["result"]["reviews"])))

    new_reviews = 0
    for rev in res["result"]["reviews"]:
        author_name = rev["author_name"]
        rating = rev["rating"]
        text = rev.get("text", "")
        users = User.objects(name__exact=author_name)
        if len(users) == 0:
            pw = gen_random_pw()
            hasher = PasswordHasher()
            pw_hash = hasher.hash(pw)
            email = gen_random_email()
            user = User(name=author_name,
                        email=email,
                        password=pw_hash)
            user.save()
        else:
            user = users[0]
            existing_review = Review.objects(user_id__exact=user.id,
                                             place_id__exact=place.id)
            if len(existing_review) > 0:
                continue

        review = Review(user_id=user.id,
                        place_id=place.id,
                        rating=rating,
                        text=text)
        review.save()
        new_reviews += 1

    print("\tNew reviews: {}".format(new_reviews))


if __name__ == "__main__":
    client = app.create_app()
    TIME_DELAY = 1.2
    N_QUERIES = 1500
    api_key = "AIzaSyDtlpG0YZrvbKJ2U2BAnEfCq0nY8Gi7zTk"

    q = 0
    places = Place.objects
    for pl in places:
        if pl.reviews_fetched:
            continue
        query_reviews_for_place(pl, api_key)
        pl.reviews_fetched = True
        pl.save()

        q += 1
        if q >= N_QUERIES:
            break
        time.sleep(TIME_DELAY)

