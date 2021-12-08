from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from flaskapp.models.user import User
from bson.objectid import ObjectId, InvalidId
from mongoengine.errors import DoesNotExist
from mongoengine import QuerySet
from flaskapp.models.place import Place
from flaskapp.models.review import Review
from flaskapp.models.user import User
from flaskapp.assets.defaults import default_img


import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np
import random
import string
import copy
import time
import base64

class RecommendationApi(Resource):

    # alapértelmezetten 5-t ajánlást ad vissza, ezt lehet paraméterként megadni
    @jwt_required()
    def get(self, count=9):
        if type(count) != int:
            try:
                count = int(count)
            except ValueError:
                return jsonify(msg="wrong number format for count")

        user_id = current_user.id  # remélem ez jó így
        num_of_neighbors = 3  # ezt lehet változtatni, de szerintem ez így most elég valszeg

        data, place_ids = self.prepare_datastructure()


        # felhasználó ajálásai, ha mindenkit figyelembe veszünk:
        df = pd.DataFrame(data, index=place_ids)
        df1 = df.copy()
        global_personal_bests = self.place_recommender(user_id, num_of_neighbors, count, df, df1)

        #felhasználó ajánlásai, ha csak a barátait vesszük figyelembe:
        u_friends_ids = [friend for friend in current_user.friends]  # current_user barátai
        u_friends_ids.append(current_user.id)  # őt is beletesszük
        df = pd.DataFrame(data, index=place_ids)
        df = df[np.array(u_friends_ids)]
        df1 = df.copy()
        global_personal_friends_bests = self.place_recommender(user_id, num_of_neighbors, count, df, df1)

        # a current_user .től független legjobban értékelt helyek (azokat, amiket ő már értékelt, nem tekinti)

        df = pd.DataFrame(data, index=place_ids)
        a = df[df.columns.values[0]].to_numpy()
        places_tried = np.nonzero(a)[0]
        b = np.array(list(range(len(a))))
        places_not_tried = np.setdiff1d(b, places_tried)
        data = df.iloc[places_not_tried].to_numpy()
        rows = np.sum(data, axis=1) / (np.count_nonzero(data, axis=1)+np.finfo(float).eps)
        bests = np.argsort(rows)[::-1]

        global_bests = {}
        for i in range(count):
            global_bests[df.index.values[bests[i]]] = rows[bests[i]]

        # a három féle ajánlás merge-elése (azért jó, mert bármennyi értékelés van bármekkora felhasználó tárorral,
        # mindig a lehető legjobbat kapja

        merged_bests = {**global_bests, **global_personal_bests, **global_personal_friends_bests}
        sorted_merged_bests = sorted(merged_bests.items(), key=lambda x: x[1], reverse=True)
        sorted_merged_bests = sorted_merged_bests[:count]

        results = []
        for place_id, _ in sorted_merged_bests:
            place = Place.objects.get(id__exact=place_id)
            results.append({
                "place_id": str(place.id),
                "place_name": place.name,
                "rating": place.rating()
            })
            if len(place.pictures) > 0:
                results[-1]["picture"] = base64.b64encode(place.pictures[0]).decode("UTF-8")
            else:
                results[-1]["picture"] = default_img

            friend_revs = []
            for friend_id in current_user.friends:
                revs = Review.objects(user_id__exact=friend_id, place_id__exact=place_id)
                if len(revs) > 0:
                    friend = User.objects.get(id__exact=friend_id)
                    friend_revs.append({
                        "name": friend.name,
                        "rating": revs[0].rating
                    })

            if friend_revs:
                results[-1]["friend_ratings"] = friend_revs[:3]

        return jsonify({"recommendations": results})



    #EZT NE BÁNTSÁTOK:
    def prepare_datastructure(self):
        good_users = set([current_user.id] + [u for u in current_user.friends])
        good_places = set()
        selected_reviews = []
        for uid in good_users:
            for review in Review.objects(user_id__exact=uid):
                selected_reviews.append(review)
                good_places.add(review["place_id"])

        N_REVIEWS = 400
        for review in Review.objects.aggregate([{"$sample": {"size": N_REVIEWS}}]):
            good_users.add(review["user_id"])
            good_places.add(review["place_id"])
            selected_reviews.append(review)

        place_ids = np.unique(np.array(list(good_places)))
        user_ids = np.unique(np.array(list(good_users)))
        data = {user_id: [0] * len(place_ids) for user_id in user_ids}
        place_idx = {place_id: i for i, place_id in enumerate(place_ids)}

        for review in selected_reviews:
            data[review["user_id"]][place_idx[review["place_id"]]] = review["rating"]
        return data, place_ids

    #EZT NE BÁNTSÁTOK:
    def recommend_places(self, user, num_recommended_places, df, df1):
        recommended_places = []

        for m in df[df[user] == 0].index.tolist():
            index_df = df.index.tolist().index(m)
            predicted_rating = df1.iloc[index_df, df1.columns.tolist().index(user)]
            recommended_places.append((m, predicted_rating))

        sorted_rm = sorted(recommended_places, key=lambda x: x[1], reverse=True)

        rank = 1
        personal_bests = {}
        for recommended_place in sorted_rm[:num_recommended_places]:
            personal_bests[recommended_place[0]] = recommended_place[1]
            rank = rank + 1

        return personal_bests

    #EZT NE BÁNTSÁTOK:
    def place_recommender(self, user, num_neighbors, num_recommendation, df, df1):
        number_neighbors = num_neighbors

        knn = NearestNeighbors(metric='cosine', algorithm='auto')
        knn.fit(df.values)
        distances, indices = knn.kneighbors(df.values, n_neighbors=number_neighbors)

        user_index = df.columns.tolist().index(user)

        for m, t in list(enumerate(df.index)):
            if df.iloc[m, user_index] == 0:
                sim_places = indices[m].tolist()
                place_distances = distances[m].tolist()

                if m in sim_places:
                    id_place = sim_places.index(m)
                    sim_places.remove(m)
                    place_distances.pop(id_place)

                else:
                    sim_places = sim_places[:number_neighbors - 1]
                    place_distances = place_distances[:number_neighbors - 1]

                place_similarity = [1 - x for x in place_distances]
                place_similarity_copy = place_similarity.copy()
                nominator = 0

                for s in range(0, len(place_similarity)):
                    if df.iloc[sim_places[s], user_index] == 0:
                        if len(place_similarity_copy) == (number_neighbors - 1):
                            place_similarity_copy.pop(s)

                        else:
                            place_similarity_copy.pop(s - (len(place_similarity) - len(place_similarity_copy)))

                    else:
                        nominator = nominator + place_similarity[s] * df.iloc[sim_places[s], user_index]

                if len(place_similarity_copy) > 0:
                    if sum(place_similarity_copy) > 0:
                        predicted_r = nominator / sum(place_similarity_copy)

                    else:
                        predicted_r = 0

                else:
                    predicted_r = 0

                df1.iloc[m, user_index] = predicted_r
        return self.recommend_places(user, num_recommendation, df, df1)
