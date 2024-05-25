from recommend import recommend

recommend.create_and_save_tfidf_matrix_v1()
user_id = 1
recommend.create_and_save_user_profile(user_id, 'v1')
recommend.calculate_and_save_similarity_matrix(user_id,'v1')
print(recommend.get_recommendations(user_id))
print()
recommend.update_user_and_similarity_matrix(user_id,'The Dark Knight Rises','buy','v1')
print(recommend.get_recommendations(user_id))
