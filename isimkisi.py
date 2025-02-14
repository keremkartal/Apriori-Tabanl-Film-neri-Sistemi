import pandas as pd

class MovieRecommendation:
    def __init__(self):
        self.df = pd.read_csv('filtered_tagg.csv')
        self.genome_tags_df = pd.read_csv('genome_tags.csv')
        self.movies_df = pd.read_csv('movie.csv')
        self.genome_scores_df = pd.read_csv('genome_scores.csv')

    def check_movie_watched(self, user_id, movie_title):
        results = []
        movie_id_row = self.movies_df[self.movies_df['title'].str.lower() == movie_title.lower()]

        if not movie_id_row.empty:
            movie_id = movie_id_row['movieId'].values[0]

            user_id = int(user_id)
            
            user_movies = self.df[self.df['userId'] == user_id]

            if movie_id in user_movies['movieId'].tolist():
                
                tag_value = user_movies[user_movies['movieId'] == movie_id]['tag'].values[0]
                
                tag_id_values = self.genome_tags_df[self.genome_tags_df['tag'] == tag_value]['tagId'].values

                if len(tag_id_values) > 0:
                    tag_id = tag_id_values[0]
                    relevance_results = self.relevancehesapla(tag_id)
                    results.extend(relevance_results)
                else:
                    results.append(f"Tag '{tag_value}' için tagId bulunamadı.")
            else:
                results[""]
        else:
            results.append(f"'{movie_title}' ismine sahip bir film bulunamadı.")
        return results
  
    def relevancehesapla(self, tag_deger):
        filtered_df = self.genome_scores_df[self.genome_scores_df['tagId'] == tag_deger]
        result_df = filtered_df[['movieId', 'relevance']]
        result_df = result_df.merge(self.movies_df[['movieId', 'title']], on='movieId', how='left')
        result_df = result_df.sort_values(by='relevance', ascending=False)
        return result_df['title'].head(50).tolist()

def kisi_film_oner(user_id, movie_title):
    onereci = MovieRecommendation()
    return onereci.check_movie_watched(user_id, movie_title)
