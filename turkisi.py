import pandas as pd

class FilmOnereci:
    def __init__(self, movies_file='top_10_genres_movies_with_all_genres2.csv', ratings_file='yeni_ratings.csv'):
        self.movies_df = pd.read_csv(movies_file)
        self.ratings_df = pd.read_csv(ratings_file)
    
    def get_recommendations(self, user_id, genre):
        user_ratings = self.ratings_df[self.ratings_df['userId'] == user_id]
        high_rated = user_ratings[user_ratings['rating'] >= 3.5]
        movie_ids = high_rated['movieId'].values
        movies_in_genre = self.movies_df[self.movies_df['genres'].str.contains(genre, case=False)]
        user_high_rated_movies = movies_in_genre[movies_in_genre['movieId'].isin(movie_ids)]
        
        watched_movie_ids = user_high_rated_movies['movieId'].values

        similar_users_ratings = self.ratings_df[
            (self.ratings_df['movieId'].isin(watched_movie_ids)) &
            (self.ratings_df['rating'] >= 3.5)
        ]


        similar_users = similar_users_ratings['userId'].unique()
        recommended_movies = self.ratings_df[
            (self.ratings_df['userId'].isin(similar_users)) &
            (self.ratings_df['movieId'].isin(movies_in_genre['movieId']))
        ]
        
        average_ratings = recommended_movies.groupby('movieId')['rating'].mean().reset_index()
        high_average_ratings = average_ratings[average_ratings['rating'] >= 3.0]

        recommended_movie_ids = high_average_ratings['movieId'].values
        recommended_movies_final = self.movies_df[self.movies_df['movieId'].isin(recommended_movie_ids)]

        
        film_names = recommended_movies_final[~recommended_movies_final['movieId'].isin(watched_movie_ids)]['title'].drop_duplicates().head(50).tolist()

        return film_names

def film_oner(user_id, genre):
    onerecii = FilmOnereci()
    return onerecii.get_recommendations(user_id, genre)
