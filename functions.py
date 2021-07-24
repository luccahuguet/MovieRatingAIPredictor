from my_data import *
import numpy as np
import pandas as pd
import json
import csv


def format_input(inputs, data_genres, counter):
    data_genres = data_genres.replace("'", '"')
    data_genres = json.loads(data_genres)
    row_genres = []
    for genre in data_genres:
        row_genres.append(genre["name"])

    for idx, gen in enumerate(genre_types):
        inputs.loc[counter][idx] = 1 if gen in row_genres else 0
    return inputs


def format_input2(user_specific_movie_data):

    inputs = pd.DataFrame(
        np.zeros((len(user_specific_movie_data), len(my_params))),
        index=range(0, (len(user_specific_movie_data))),
        columns=my_params,
    )

    for counter, user_data_row in enumerate(user_specific_movie_data):

        data_genres = user_data_row["genres"]
        data_genres = data_genres.replace("'", '"')
        data_genres = json.loads(data_genres)

        row_genres = []
        for genre in data_genres:
            row_genres.append(genre["name"])

        # print(f"row_genres = {row_genres}")
        for c5, gen in enumerate(genre_types):
            # print(f"gen  = {gen}")
            inputs.loc[counter][gen] = 1 if gen in row_genres else 0
        for num_param in continuous_params:
            inputs.loc[counter][num_param] = user_data_row[num_param]
    return inputs


def calc_ratings_per_user(ratings, userId):
    ratings[int(userId)] += 1
    return ratings


def get_user_ratings(ratings_per_user, chosen_user):
    lower_limit = 0

    with open(rat_small, newline="", errors="ignore") as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=",")
        for counter, row in enumerate(spamreader):
            if counter > lower_limit and chosen_user == int(row["userId"]):
                row["rating"] = str(float(row["rating"]) / 5.0)
                ratings_per_user.append(row)
        return ratings_per_user


def get_movie_data():
    lower_limit = 0
    movie_data = []

    with open(mov, newline="", errors="ignore") as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=",")
        for counter, row in enumerate(spamreader):
            if counter > lower_limit:
                movie_data.append(row)
    return movie_data


def get_user_specific_movie_data(user_specific_ratings, movie_data):
    lower_limit = 0
    counter2 = 0
    inputs = []

    user_specific_movie_data = []  # [""] * len(user_specific_ratings)

    for counter, this_rating in enumerate(user_specific_ratings):
        movie_data_row = [
            row for row in movie_data if row["id"] == this_rating["movieId"]
        ]
        if movie_data_row:
            counter2 += 1
            movie_data_row = movie_data_row[0]
            this_rating.update(movie_data_row)
            user_specific_movie_data.append(this_rating)

        # print(f"movie_data_row2 = {movie_data_row} \n")
        # print(user_specific_movie_data)

    return user_specific_movie_data

    # with open(mov, newline="", errors="ignore") as csvfile:
    #     spamreader = csv.DictReader(csvfile, delimiter=",")
    #     for counter, row in enumerate(spamreader):
    #         if counter > lower_limit:
    #             user_specific_movie_data.append(row)
    #     return user_specific_movie_data
