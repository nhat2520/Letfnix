get_recommendations(userId, tfidf_matrix_filename):
tfidf_matrix = tf.fit_transform(data['description'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)#?
titles = data['original_title']
indices = pd.Series(data.index, index=data['original_title'])
#save the tf idf vectorizer and count vectorizer and tf-idf matrix
with open('tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(tf, f)
save_npz('tfidf_matrix.npz', tfidf_matrix)
#create new user profile
tfidf_matrix = load_npz('tfidf_matrix.npz')

# Create a new user profile based on the average of the TF-IDF matrix
user_profile = np.mean(tfidf_matrix.toarray(), axis=0)

# Save the user profile
with open('user_profile.pkl', 'wb') as f:
    pickle.dump(user_profile, f)

# Calculate the cosine similarity between the user profile and the TF-IDF matrix
user_profile = user_profile.reshape(1, -1)
cosine_sim = cosine_similarity(user_profile, tfidf_matrix)
# Save the cosine similarity matrix
save_npz('cosine_sim.npz', csr_matrix(cosine_sim))

#use cosine matrix to get recommendations








#create user profile with ratings
'''
def create_user_profile(userId, cosine_sim, user_ratings_matrix):
    user_ratings = user_ratings_matrix.loc[userId].dropna()
    profile_vector = np.zeros_like(cosine_sim[0])
    for movieId, rating in user_ratings.items():
        # Check if the movie exists in the data DataFrame
        if movieId in data['id'].values:
            # Get the index of the movie in the cosine similarity matrix
            idx = data[data['id'] == movieId].index[0]
            # Update the profile vector by adding the weighted similarity scores
            profile_vector += cosine_sim[idx] * rating
    return profile_vector
def normalize_vector(vector):
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm
'''
#save user profile

def weighted_rating(x):
    v = x['vote_count']
    R = x['vote_average']
    return (v/(v+m) * R) + (m/(m+v) * C)

def save_user_profile(user_profile, file_path, file_format='pkl'):
    if file_format == 'pkl':
        # Save as pickle file
        with open(file_path, 'wb') as f:
            pickle.dump(user_profile, f)
    elif file_format == 'csv':
        # Save as CSV file
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(user_profile)

#use userprofile to get movies
#sget similar movies
def get_recommendations(title, length):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:length+1]
    movie_indices = [i[0] for i in sim_scores]
    return titles.iloc[movie_indices]
#recommendations taking popularity and ratings into account
vote_counts = data[data['vote_count'].notnull()]['vote_count'].astype('int')
vote_averages = data[data['vote_average'].notnull()]['vote_average'].astype('int')
C = vote_averages.mean()
data['year'] = pd.to_datetime(data['release_date'])
data['year']= data['year'].apply(
    lambda x: str(x).split('-')[0] if x != np.nan else np.nan)
m = vote_counts.quantile(0.95)
qualified = data[(data['vote_count'] >= m) & 
               (data['vote_count'].notnull()) & 
               (data['vote_average'].notnull())][['original_title', 
                                                'release_date', 
                                                'vote_count', 
                                                'vote_average', 
                                                'popularity', 
                                                'genres']]

qualified['vote_count'] = qualified['vote_count'].astype('int')
qualified['vote_average'] = qualified['vote_average'].astype('int')
qualified['wr'] = qualified.apply(weighted_rating, axis=1)
qualified = qualified.sort_values('wr', ascending=False).head(250)

def improved_recommendations(title, length):
    # Compute similarity between user profile and items
    similarity_scores = np.dot(user_profile, cosine_sim)
    
    # Get indices of top N similar items
    top_indices = np.argsort(similarity_scores)[0][-top_n:][::-1]
    
    # Get movie titles for the top recommended indices
    recommended_movies = movies_df.iloc[top_indices]['title']
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:length]
    movie_indices = [i[0] for i in sim_scores]
    
    movies = data.iloc[movie_indices][['original_title', 'vote_count', 'vote_average', 'release_date']]
    vote_counts = movies[movies['vote_count'].notnull()]['vote_count'].astype('int')
    vote_averages = movies[movies['vote_average'].notnull()]['vote_average'].astype('int')
    C = vote_averages.mean()
    m = vote_counts.quantile(0.60)
    qualified = movies[(movies['vote_count'] >= m) & (movies['vote_count'].notnull()) & 
                       (movies['vote_average'].notnull())]
    qualified['vote_count'] = qualified['vote_count'].astype('int')
    qualified['vote_average'] = qualified['vote_average'].astype('int')
    qualified['wr'] = qualified.apply(weighted_rating, axis=1)
    qualified = qualified.sort_values('wr', ascending=False).head(10)
    return qualified

with open('tfidf_vectorizer.pkl', 'rb') as f:
    tfidf = pickle.load(f)

cosine_sim_sparse = load_npz('cosine_sim.npz')
cosine_sim = cosine_sim_sparse.toarray()

# Assume tfidf_matrix is already computed and available
tfidf_matrix = tfidf.transform(movies_df['description'])

# Function to create a popular movies profile for new users
def create_popular_movies_profile(ratings_df, movies_df, tfidf_matrix, top_n=10):
    # Calculate average ratings for each movie
    avg_ratings = ratings_df.groupby('movieId')['rating'].mean()
    
    # Get the top N movies by average rating
    top_movies = avg_ratings.nlargest(top_n).index
    
    # Initialize the profile vector
    profile_vector = np.zeros(tfidf_matrix.shape[1])
    
    # Sum the TF-IDF vectors of the top movies
    for movieId in top_movies:
        movie_idx = movies_df[movies_df['movieId'] == movieId].index[0]
        profile_vector += tfidf_matrix[movie_idx]
    
    # Normalize the profile vector
    profile_vector = normalize(profile_vector.reshape(1, -1))
    
    return profile_vector
#look for ways to create a profile with avg of all movies
generic_user_profile = create_popular_movies_profile(ratings_df, movies_df, tfidf_matrix)

#change user profile based on action
def change_up_view(user_profile, movie):
    return nan
def change_up_buy(user_profile, movie):
    return nan