"""Python file to create/save user and item profiles, get recommendations for user"""

import pickle
import warnings
import os

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix, load_npz, save_npz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

warnings.simplefilter("ignore")


# Function to create and save the TF-IDF matrix
def create_and_save_tfidf_matrix_v1():
    """
    Create and save a TF-IDF matrix from the given data.

    Args:
        filename (str): The filename for saving the TF-IDF model and matrix.

    Saves:
        tfidf_v1.pkl: Pickle file containing the fitted TfidfVectorizer model.
        tfidf_matrix_v1.npz: NPZ file containing the TF-IDF matrix.
    """
    directory = "server/repo"  
    tfidf_pkl_path = os.path.join(directory, "tfidf_v1.pkl")
    tfidf_matrix_path = os.path.join(directory, "tfidf_matrix_v1.npz")
    
    # Check if the files already exist
    if os.path.exists(tfidf_pkl_path) and os.path.exists(tfidf_matrix_path):
        return

    os.makedirs(directory, exist_ok=True)
    data = pd.read_csv('server/recommend/data.csv')
    data['tagline'] = data['tagline'].fillna('')
    data['description'] = data['overview'] + data['tagline']
    data['description'] = data['description'].fillna('')
    tf = TfidfVectorizer(
        analyzer="word", ngram_range=(1, 2), min_df=0.01, stop_words="english"
    )
    tfidf_matrix = tf.fit_transform(data['description'])
    with open("server/repo/tfidf_v1.pkl", "wb") as f:
        pickle.dump(tf, f)
    save_npz("server/repo/tfidf_matrix_v1.npz", tfidf_matrix)


# Function to create a new user profile and save it
def create_and_save_user_profile(user_id, tfidf_matrix_filename):
    """
    Create and save a user profile based on the TF-IDF matrix.

    Args:
        user_id (int): The user ID for the profile.
        tfidf_matrix_filename (str): The filename of the saved TF-IDF matrix.

    Saves:
        user_profile_{user_id}.pkl: Pickle file containing the user profile vector.
    """

    tfidf_matrix = load_npz(f"server/repo/tfidf_matrix_{tfidf_matrix_filename}.npz")
    user_profile = np.mean(tfidf_matrix.toarray(), axis=0)
    with open(f"server/repo/user_profile_{user_id}.pkl", "wb") as f:
        pickle.dump(user_profile, f)


# Function to calculate and save the cosine similarity matrix
def calculate_and_save_similarity_matrix(user_id, tfidf_matrix_filename):
    """
    Calculate and save the cosine similarity matrix for a user profile.

    Args:
        user_id (int): The user ID for which to calculate the similarity matrix.
        tfidf_matrix_filename (str): The filename of the saved TF-IDF matrix.

    Saves:
        sim_matrix_{user_id}.npz: NPZ file containing the cosine similarity matrix.
    """

    with open(f"server/repo/user_profile_{user_id}.pkl", "rb") as f:
        user_profile = pickle.load(f)
    tfidf_matrix = load_npz(f"server/repo/tfidf_matrix_{tfidf_matrix_filename}.npz")
    user_profile = user_profile.reshape(1, -1)
    cosine_sim = linear_kernel(user_profile, tfidf_matrix)
    save_npz(f"server/repo/sim_matrix_{user_id}.npz", csr_matrix(cosine_sim))


# Function to get recommendations based on a user_id
def get_recommendations(user_id, length):
    """
    Get the top 5 recommendations for a user based on the cosine similarity matrix.

    Args:
        user_id (int): The user ID for which to get recommendations.
        length (int): numnber of movies to return.

    Returns:
        list of int: The indices of the top 5 recommended items.
    """

    cosine_sim = load_npz(f"server/repo/sim_matrix_{user_id}.npz").toarray()
    top_n_indices = cosine_sim[0].argsort()[-length:-1][::-1]  # Top 5 recommendations
    data = pd.read_csv('server/recommend/data.csv')
    return data.iloc[top_n_indices]


# Function to update user profile and cosine similarity matrix
def update_user_and_similarity_matrix(
    user_id, movie_name, action, tfidf_matrix_filename
):
    """
    Update the user profile and cosine similarity matrix based on user actions.

    Args:
        user_id (int): The user ID for which to update the profile and similarity matrix.
        movie_name (str): The name of the movie.
        action (str): The action performed by the user ('view' or 'buy').
        tfidf_matrix_filename (str): The filename of the saved TF-IDF matrix.
    """
    def update_user_profile(user_profile, tfidf_vector, action):
        if action == "view":
            weight = 0.1  # Define a smaller weight for viewing
        elif action == "buy":
            weight = 0.5  # Define a larger weight for buying
        else:
            raise ValueError("Unknown action")
        user_profile = user_profile * (1 - weight) + tfidf_vector * weight
        return user_profile / np.linalg.norm(user_profile)

    with open(f"server/repo/user_profile_{user_id}.pkl", "rb") as f:
        user_profile = pickle.load(f)
    
    data = pd.read_csv('server/recommend/data.csv')
    movie_idx =  data.index[data['original_title'] == movie_name].tolist()

    tfidf_matrix = load_npz(f"server/repo/tfidf_matrix_{tfidf_matrix_filename}.npz")
    movie_tfidf_vector = tfidf_matrix[movie_idx].toarray().flatten()
    user_profile = update_user_profile(user_profile, movie_tfidf_vector, action)

    with open(f"server/repo/user_profile_{user_id}.pkl", "wb") as f:
        pickle.dump(user_profile, f)

    user_profile = user_profile.reshape(1, -1)
    updated_cosine_sim = linear_kernel(user_profile, tfidf_matrix)
    save_npz(f"server/repo/sim_matrix_{user_id}.npz", csr_matrix(updated_cosine_sim))



#code should look something like this

create_and_save_tfidf_matrix_v1()
user_id = 1
create_and_save_user_profile(user_id, 'v1')
calculate_and_save_similarity_matrix(user_id,'v1')
print(get_recommendations(user_id))
print()
update_user_and_similarity_matrix(user_id,'The Dark Knight Rises','buy','v1')
print(get_recommendations(user_id))
