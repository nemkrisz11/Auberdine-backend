from flask import Blueprint
from flaskapp.models.review import Review
from flask_jwt_extended import jwt_required, current_user
from flaskapp.models.place import Place
from flask_restful import Resource
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np
import random
import string
import copy

bp = Blueprint("recommendation", __name__, url_prefix="")

class Recommendations(Resource):

    # alapértelmezetten 5-t ajánlást ad vissza, ezt lehet paraméterként megadni

    @bp.route("/user/recommendations")
    @jwt_required()
    def fetch_recommendation(self, num_of_recs=5):
        user_id = current_user.id  # remélem ez jó így
        num_of_neighbors = 3  # ezt lehet változtatni, de szerintem ez így most elég valszeg
        reviews = Review.objects  # de lehet, hogy ez így nem azta adja vissza, ami várok
        # a review egy lista, ami Review objektumokat tartlamazzon, ennyi...


        # INNEN MÁR NE PISZKÁLJUNK SEMMIT!!! még akkor se ha lassan fut (bár, ahhoz kb 10k User kellene)
        data, place_ids = self.prepare_datastructure(reviews)


        # felhasználó ajálásai, ha mindenkit figyelembe veszünk:
        df = pd.DataFrame(data, index=place_ids)
        df1 = copy.deepcopy(df)
        global_personal_bests = self.place_recommender(user_id, num_of_neighbors, num_of_recs, df, df1)

        #felhasználó ajánlásai, ha csak a barátait vesszük figyelembe:
        u_friends_ids = current_user.friends()  # current_user barátai
        u_friends_ids.append(current_user.id)  # őt is beletesszük
        df = pd.DataFrame(data, index=place_ids)  # csak őket vizsgáljuk
        df = df[np.array(u_friends_ids)]
        df1 = copy.deepcopy(df)
        global_personal_friends_bests = self.place_recommender(user_id, num_of_neighbors, num_of_recs, df, df1)

        # a current_user .től független legjobban értékelt helyek (azokat, amiket ő már értékelt, nem tekinti)
        df = pd.DataFrame(data, index =place_ids)
        a = df[df.columns.values[0]].to_numpy()
        places_tried = np.nonzero(a)[0]
        b = np.array(list(range(len(a))))
        places_not_tried = np.setdiff1d(b, places_tried)
        data = df.iloc[places_not_tried].to_numpy()
        rows = np.sum(data, axis=1) / (np.count_nonzero(data, axis=1)+np.finfo(float).eps)
        bests = np.argsort(rows)[::-1]

        global_bests = {}
        for i in range(num_of_recs):
            global_bests[df.index.values[bests[i]]] = rows[bests[i]]
            print('{0}: {1} - avg rating:{2}'.format(i, df.index.values[bests[i]], rows[bests[i]]))

        # a három féle ajánlás merge-elése (azért jó, mert bármennyi értékelés van bármekkora felhasználó tárorral,
        # mindig a lehető legjobbat kapja

        merged_bests = {**global_bests, **global_personal_bests, **global_personal_friends_bests}
        sorted_merged_bests = sorted(merged_bests.items(), key=lambda x: x[1], reverse=True)
        print(sorted_merged_bests)
        sorted_merged_bests = sorted_merged_bests[:num_of_recs]

        # EZT ITT NAGYON MEG KELL NÉZNI, HOGY MEGFELELŐ-E !!!
        result = [(Place.objects.get(id__exact=review_id)).__repr__() for review_id, score in sorted_merged_bests]
        return result

    #EZT NE BÁNTSÁTOK:
    def prepare_datastructure(self, reviews):
        place_ids = np.unique(np.array([review.place_id for review in reviews]))
        user_ids = np.unique(np.array([review.user_id for review in reviews]))

        data = {}
        for user_id in user_ids:
            user_ratings = [review.rating for review in reviews if review.user_id == user_id]
            user_places = [review.place_id for review in reviews if review.user_id == user_id]
            ratings_vec = []
            for place_id in place_ids:
                if place_id not in user_places:
                    ratings_vec.append(0)
                else:
                    index = user_places.index(place_id)
                    ratings_vec.append(user_ratings[index])
            data[user_id] = ratings_vec
        return data, place_ids

    #EZT NE BÁNTSÁTOK:
    def recommend_places(self, user, num_recommended_places, df, df1):
        print('The list of the Places {} has visited \n'.format(user))

        for m in df[df[user] > 0][user].index.tolist():
            print(m)

        print('\n')

        recommended_places = []

        for m in df[df[user] == 0].index.tolist():
            index_df = df.index.tolist().index(m)
            predicted_rating = df1.iloc[index_df, df1.columns.tolist().index(user)]
            recommended_places.append((m, predicted_rating))

        sorted_rm = sorted(recommended_places, key=lambda x: x[1], reverse=True)

        print('The list of the Recommended places \n')
        rank = 1
        personal_bests = {}
        for recommended_place in sorted_rm[:num_recommended_places]:
            personal_bests[recommended_place[0]] = recommended_place[1]
            print('{}: {} - predicted rating:{}'.format(rank, recommended_place[0], recommended_place[1]))
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
