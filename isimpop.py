import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import time

class MovieRecommender:
    def __init__(self):
        self.tag_df = pd.read_csv("tag.csv")
        self.genome_tags_df = pd.read_csv("genome_tags.csv")
        self.movie_df = pd.read_csv("movie.csv")
        self.genome_scores_df = pd.read_csv("genome_scores.csv")

    def get_recommendations(self, film_name):
        start_time = time.time()  

        movie_id_row = self.movie_df[self.movie_df['title'].str.lower() == film_name.lower()]

        if not movie_id_row.empty:
            movie_id = movie_id_row['movieId'].values[0]
        else:
            print("Film not found.")
            return []

        relevant_tags = self.genome_scores_df[self.genome_scores_df['movieId'] == movie_id].nlargest(10, 'relevance')
        tag_ids = relevant_tags['tagId'].tolist()

        relevant_movies = self.genome_scores_df[self.genome_scores_df['tagId'].isin(tag_ids) & (self.genome_scores_df['relevance'] > 0.4)]
        relevant_movie_ids = relevant_movies['movieId'].unique()

        combined_df = self.tag_df[self.tag_df['movieId'].isin(relevant_movie_ids)]
        
        pivot_table = combined_df.pivot_table(index='userId', columns='movieId', values='tag', aggfunc='count', fill_value=0)
        
        print(f"Pivot Tablo Boyutu: {pivot_table.shape}")

        pivot_table = pivot_table.apply(lambda x: x.map(lambda y: True if y > 0 else False))

        frequent_itemsets = apriori(pivot_table, min_support=0.01, use_colnames=True)
        
        print(f"Apriori Eleman Sayısı: {len(frequent_itemsets)}")
        print(f"Apriori Sonuçları: \n{frequent_itemsets.head()}")

        rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)

        print(f"Association Kuralları Sayısı: {len(rules)}")
        print(f"Association Kuralları: \n{rules.head()}")
   
        recommended_movies = rules.sort_values(by='lift', ascending=False)['consequents']
        recommended_movie_ids = [list(conseq)[0] for conseq in recommended_movies]
        recommended_movie_titles = self.movie_df[self.movie_df['movieId'].isin(recommended_movie_ids)]['title']

        end_time = time.time()  
        print(f" {film_name} film araması : {end_time - start_time:.2f} saniyede sürdü") 

        return recommended_movie_titles.tolist()

def populer_film_oner(film_title):
    recommender = MovieRecommender()
    return recommender.get_recommendations(film_title)
