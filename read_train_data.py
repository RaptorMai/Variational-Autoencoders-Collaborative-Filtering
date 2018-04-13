import os, sys
import pandas as pd
import numpy as np
import random
import pickle
from scipy import sparse
DATA_DIR = '/home/gupta_kilol1/Adv-ML/project/ml-20m'
raw_data = pd.read_csv(os.path.join(DATA_DIR, 'ratings.csv'), header=0)

unique_user_ids = raw_data.userId.unique()
random.shuffle(unique_user_ids) # to ensure random splitting between train, val and test
unique_movie_ids = raw_data.movieId.unique()

number_of_users = len(unique_user_ids)
print("number of users: ", number_of_users)

number_of_movies = len(unique_movie_ids)
print("number of movies: ", number_of_movies)
# check why this number is less

# split users into training, validation and test
val_user_ids = []
test_user_ids = []
train_user_ids = []

for i in range(10000):
    val_user_ids.append(unique_user_ids[i]) # first 10k after shuffling keys

for i in range(10000, 20000):
    test_user_ids.append(unique_user_ids[i]) # next 10k after shuffling keys

for i in range(20000, number_of_users): # all the remaining form training data
    train_user_ids.append(unique_user_ids[i])

print("number of training users: ", len(train_user_ids))

# creating a movieId and userId to index dictionary for creating train_data ndarray
user2id = {}
movie2id = {}
user2id = dict((uid, i) for (i, uid) in enumerate(train_user_ids))
movie2id = dict((mid, i) for (i, mid) in enumerate(unique_movie_ids))

print("creating training data....")

rows = []
cols = []
for u_id in train_user_ids:
	print(user2id[u_id])
	m_ids = raw_data[(raw_data.userId == u_id) & (raw_data.rating > 3.5)]['movieId'].tolist()
	movie_indexes = [movie2id[m] for m in m_ids]
	rows.extend([user2id[u_id] for i in range(len(m_ids))])
	cols.extend(movie_indexes)

pickle.dump(rows, open("rows.file", "wb"))
pickle.dump(cols, open("cols.file", "wb"))


# creating a sparse matrix with no_of_train_users X movies for training, binarized feedback
# rows and cols should be of same length
train_data = sparse.csr_matrix((np.ones_like(rows),(np.array(rows), np.array(cols))), dtype='float64', shape=(len(train_user_ids), number_of_movies))

# dumping variable to load later for use in VAE code
pickle.dump(train_data, open("train_data.file", "wb"))