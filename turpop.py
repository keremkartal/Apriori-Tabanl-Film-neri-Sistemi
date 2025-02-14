
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import time


class MovieRecommender:
    def __init__(self, tag_file='tag.csv', movie_file='yeni_movies.csv', rating_file='yeni_ratings.csv'):
        self.tag_df = pd.read_csv(tag_file)  
        self.movie_df = pd.read_csv(movie_file) 
        self.rating_df = pd.read_csv(rating_file) 

    def get_tur(self, film_türü):
        start_time = time.time()

        relevant_movies = self.movie_df[self.movie_df['genres'].str.contains(film_türü, case=False, na=False)]
        relevant_movie_ids = relevant_movies['movieId'].tolist()

        combined_df = self.tag_df[self.tag_df['movieId'].isin(relevant_movie_ids)]

        pivot_table = combined_df.pivot_table(index='userId', columns='movieId', values='tag', aggfunc='count', fill_value=0)
        
        pivot_table = pivot_table.apply(lambda x: x.map(lambda y: True if y > 0 else False))

        print(f"Pivot Tablo Boyutu: {pivot_table.shape}")

        print(f"Pivot Tablo: \n{pivot_table.head()}")  

        frequent_itemsets = apriori(pivot_table, min_support=0.009, use_colnames=True)

        print(f"Apriori Eleman Sayısı: {len(frequent_itemsets)}")

        print(f"Apriori Sonuçları: \n{frequent_itemsets.head()}")

        rules = association_rules(frequent_itemsets, metric="lift", min_threshold=0.1)


        print(f"Association Kuralları Sayısı: {len(rules)}")
        print(f"Association Kuralları: \n{rules.head()}")

        top_50_recommendations = rules.sort_values('lift', ascending=False)

        recommended_movie_ids = top_50_recommendations['consequents'].apply(lambda x: list(x)[0]).tolist()

        recommended_movies = self.movie_df[self.movie_df['movieId'].isin(recommended_movie_ids)]

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f" {elapsed_time:.2f} seconds")
        titles_list = recommended_movies['title'].tolist()
        print(f"Önerilen film sayısı: {len(titles_list)}") 

        return titles_list  

def populer_tur_oner(film_türü):
    recommender = MovieRecommender()  
    return recommender.get_tur(film_türü)
