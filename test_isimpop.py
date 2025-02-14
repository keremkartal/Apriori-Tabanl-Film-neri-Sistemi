import pytest
from isimpop import MovieRecommender

@pytest.fixture(scope="module")
def recommender():
    return MovieRecommender()

def test_valid_movie_recommendation(recommender):
    film_name = "Toy Story (1995)" 
    recommendations = recommender.get_recommendations(film_name)
    assert len(recommendations) > 0, "Mevcut bir film adı için öneri bulunamadı"


def test_invalid_movie_name(recommender):
    film_name = "Geçersiz Film Adı"
    recommendations = recommender.get_recommendations(film_name)
    assert recommendations == [], "Geçersiz bir film adı için öneri döndürülmemeli"

def test_performance(recommender):
    film_name = "Toy Story (1995)"
    import time
    start_time = time.time()
    recommender.get_recommendations(film_name)
    end_time = time.time()
    elapsed_time = end_time - start_time
    assert elapsed_time < 20, f"Öneri süresi çok uzun sürdü: {elapsed_time} saniye"

