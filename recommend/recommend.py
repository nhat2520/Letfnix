import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from scipy.sparse import save_npz
import ast 
from scipy import stats
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
import warnings; warnings.simplefilter('ignore')
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import save_npz, load_npz, csr_matrix
import pickle

# Function to create and save the TF-IDF matrix
def create_and_save_tfidf_matrix_v1(documents, filename):
    tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0.01, stop_words='english')
    tfidf_matrix = tf.fit_transform(documents)
    with open(f'tfidf_{filename}.pkl', 'wb') as f:
        pickle.dump(tf, f)
    save_npz(f'tfidf_matrix_{filename}.npz', tfidf_matrix)

# Function to create a new user profile and save it
def create_and_save_user_profile(userId, tfidf_matrix_filename):
    tfidf_matrix = load_npz(f'tfidf_matrix_{tfidf_matrix_filename}.npz')
    user_profile = np.mean(tfidf_matrix.toarray(), axis=0)
    with open(f'user_profile_{userId}.pkl', 'wb') as f:
        pickle.dump(user_profile, f)

# Function to calculate and save the cosine similarity matrix
def calculate_and_save_similarity_matrix(userId, tfidf_matrix_filename):
    with open(f'user_profile_{userId}.pkl', 'rb') as f:
        user_profile = pickle.load(f)
    tfidf_matrix = load_npz(f'tfidf_matrix_{tfidf_matrix_filename}.npz')
    user_profile = user_profile.reshape(1, -1)
    cosine_sim = linear_kernel(user_profile, tfidf_matrix)
    save_npz(f'sim_matrix_{userId}.npz', csr_matrix(cosine_sim))

# Function to get recommendations based on a userId
def get_recommendations(userId, tfidf_matrix_filename):
    cosine_sim = load_npz(f'sim_matrix_{userId}.npz').toarray()
    top_n_indices = cosine_sim[0].argsort()[-5:][::-1]  # Top 5 recommendations
    return top_n_indices

# Function to update user profile and cosine similarity matrix
def update_user_and_similarity_matrix(userId, movie_idx, action, tfidf_matrix_filename):
    def update_user_profile(user_profile, tfidf_vector, action):
        if action == "view":
            weight = 0.1  # Define a smaller weight for viewing
        elif action == "buy":
            weight = 0.5  # Define a larger weight for buying
        else:
            raise ValueError("Unknown action")
        user_profile = user_profile * (1 - weight) + tfidf_vector * weight
        return user_profile / np.linalg.norm(user_profile)

    with open(f'user_profile_{userId}.pkl', 'rb') as f:
        user_profile = pickle.load(f)
    tfidf_matrix = load_npz(f'tfidf_matrix_{tfidf_matrix_filename}.npz')
    movie_tfidf_vector = tfidf_matrix[movie_idx].toarray().flatten()
    user_profile = update_user_profile(user_profile, movie_tfidf_vector, action)
    with open(f'user_profile_{userId}.pkl', 'wb') as f:
        pickle.dump(user_profile, f)
    user_profile = user_profile.reshape(1, -1)
    updated_cosine_sim = linear_kernel(user_profile, tfidf_matrix)
    save_npz(f'sim_matrix_{userId}.npz', csr_matrix(updated_cosine_sim))

data = pd.read_csv('recommend\data.csv')
ratings = pd.read_csv('recommend\shortened_ratings.csv')
create_and_save_tfidf_matrix_v1(data['description'],'v1')
create_and_save_user_profile(1, 'v1')
calculate_and_save_similarity_matrix(1, 'v1')

print(data.loc[get_recommendations(1, 'v1')]['original_title'])

update_user_and_similarity_matrix(1, 1, 'view', 'v1')
update_user_and_similarity_matrix(1, 2, 'buy', 'v1')

print(data.loc[get_recommendations(1, 'v1')]['original_title'])
