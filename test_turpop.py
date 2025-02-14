import pytest
from turpop import MovieRecommender, populer_tur_oner
import time

def test_movie_recommender_initialization():
    try:
        recommender = MovieRecommender()
        assert recommender.tag_df is not None
        assert recommender.movie_df is not None
        assert recommender.rating_df is not None
    except FileNotFoundError:
        pytest.fail("Veri dosyaları bulunamadı. Lütfen dosya yollarını kontrol edin.")

    

def test_get_tur():
    recommender = MovieRecommender()
    genre = "Comedy"  
    recommended_movies = recommender.get_tur(genre)

    assert isinstance(recommended_movies, list), "Öneriler bir liste değil."
    assert len(recommended_movies) > 0, "Hiç öneri yok."
    for movie in recommended_movies:
        assert isinstance(movie, str), "Film başlığı bir string değil."

def test_performance():
    recommender = MovieRecommender()
    genre = "Action"
    start_time = time.time()
    recommender.get_tur(genre)
    end_time = time.time()
    assert (end_time - start_time) < 5, "Öneri süresi çok uzun."

def test_populer_tur_oner():
    genre = "Drama"
    recommendations = populer_tur_oner(genre)
    assert isinstance(recommendations, list), "Fonksiyon bir liste döndürmüyor."
    assert len(recommendations) > 0, "Hiç öneri dönmedi."
