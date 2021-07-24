from keras.models import Sequential
from keras.layers import Dense
import csv
import json
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from my_data import *
from functions import format_input
from functions import get_user_ratings
from functions import get_movie_data
from functions import get_user_specific_movie_data
from functions import format_input2
from keras.callbacks import EarlyStopping

print("\n\nIt Begins\n\n")

# rat_small_n_lines = 10005
# n_users = 672
# Index do maior n de ratings 547

chosen_user = 547
user_n_ratings = 2391

user_specific_ratings = []

user_specific_ratings = get_user_ratings(user_specific_ratings, chosen_user)

movie_data = get_movie_data()

user_specific_movie_data = get_user_specific_movie_data(
    user_specific_ratings, movie_data
)

for continuous_param in continuous_params:
    my_params.add(continuous_param)

inputs = format_input2(user_specific_movie_data)

y_ratings = inputs["rating"]

X_inputs = inputs.drop(columns="rating")

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 150)


# targets
my_X = X_inputs

# inputs
my_y = y_ratings

print(f"my input matrix =\n {my_X} \n ")

print(f"my target matrix =\n {my_y} \n ")

model = Sequential()

n_neurons = 50

# input shape takes number of columns
model.add(Dense(n_neurons, activation="relu", input_shape=(my_X.shape[1],)))

model.add(Dense(n_neurons, activation="relu"))

model.add(Dense(1, activation="sigmoid"))

model.compile(optimizer="adam", loss="mape")

print(f"\n")

prediction = model.predict(my_X.head(1))

print(f"prediction for the movie[{my_X.index[1]}] = {prediction[0][0]} \n")

print(f"target for the movie[{my_X.index[1]}] = {my_y.head(1)}\n \n")


monitor_val_acc = EarlyStopping(monitor="val_loss", patience=20)

h_callback = model.fit(
    my_X, my_y, epochs=100, validation_split=0.2, callbacks=[monitor_val_acc]
)

plt.figure(1)
plt.plot(h_callback.history["loss"])
plt.plot(h_callback.history["val_loss"])
plt.title("Model loss")
plt.ylabel("Loss")
plt.xlabel("Epoch")
plt.legend(["Train", "Test"], loc="upper right")
plt.show()

print("\n\nIt Ends\n\n")
