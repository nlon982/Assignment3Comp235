from datetime import datetime

import pytest

from CS235Flix.adapters.database_repository import SqlAlchemyRepository


from CS235Flix.movies_blueprint import services

from CS235Flix.domain.movie import Movie
from CS235Flix.domain.director import Director
from CS235Flix.domain.actor import Actor
from CS235Flix.domain.genre import Genre
from CS235Flix.domain.review import Review
from CS235Flix.domain.user import User

@pytest.fixture
def a_movie(): # these values are half made up
    a_movie = Movie("Guardians", 2014)
    a_movie.runtime_minutes = 100
    a_movie.description = "descriptiongoeshere"
    a_movie.director = Director("James Gunn")
    a_movie.actors = [Actor("Chris Pratt"), Actor("Vin Diesel"), Actor("Bradley Cooper")]
    a_movie.genres = [Genre("Action"), Genre("Adventure"), Genre("Sci-Fi")]
    a_movie.external_rating = 8.1
    a_movie.external_rating_votes = 31204
    a_movie.revenue = 301
    a_movie.metascore = 74
    return a_movie

@pytest.fixture
def a_review():
    a_review = Review(User("Bob Dylan", "Elephant12"), Movie("Terminator", 1984), "Cool movie", 9)
    a_review.timestamp = datetime.fromisoformat("2020-02-24 12:52:30")
    return a_review

def test_movie_to_dict(a_movie):
    a_movie_dict = services.movie_to_dict(a_movie)
    assert a_movie_dict["title"] == "Guardians"
    assert a_movie_dict["release_year"] == 2014
    assert a_movie_dict["description"] == "descriptiongoeshere"
    assert a_movie_dict["director"] == "James Gunn"
    assert a_movie_dict["actors"] == "Chris Pratt, Vin Diesel, Bradley Cooper"
    assert a_movie_dict["genres"] == "Action, Adventure, Sci-Fi"
    assert a_movie_dict["external_rating"] == 8.1
    assert a_movie_dict["external_rating_votes"] == 31204
    assert a_movie_dict["revenue"] == 301
    assert a_movie_dict["metascore"] == 74


def test_movies_to_dict(a_movie):
    a_movie_dict = services.movie_to_dict(a_movie) # to compare to

    movie_list = [a_movie] * 10
    movie_dict_list = services.movies_to_dict(movie_list)

    for movie_dict in movie_dict_list:
        assert movie_dict == a_movie_dict

def test_review_to_dict(a_review):
    a_review_dict = services.review_to_dict(a_review)
    assert a_review_dict["review_text"] == "Cool movie"
    assert a_review_dict["rating"] == 9
    assert a_review_dict["timestamp"] == "2020-02-24 at 12:52:30"
    assert a_review_dict["user_name"] == "bob dylan"

def test_reviews_to_dict(a_review):
    a_review_dict = services.review_to_dict(a_review)

    review_list = [a_review] * 10
    review_dict_list = services.reviews_to_dict(review_list)

    for review_dict in review_dict_list:
        assert review_dict == a_review_dict

def test_to_string():
    a_director = Director("James Gunn")
    a_actor_1 = Actor("Ben Stiller")
    a_actor_2 = Actor("John Davies")
    a_genre_1 = Genre("Action")
    a_genre_2 = Genre("Adventure")

    assert services.director_to_string(a_director) == "James Gunn"
    assert services.actor_to_string(a_actor_1) == "Ben Stiller"
    assert services.genre_to_string(a_genre_1) == "Action"

    assert services.actors_to_string([a_actor_1, a_actor_2]) == "Ben Stiller, John Davies"
    assert services.genres_to_string([a_genre_1, a_genre_2]) == "Action, Adventure"

def test_get_all_movies(in_memory_repo): # there are 100 movies in the test data
    movie_dict_list = services.get_all_movies(in_memory_repo)
    assert len(movie_dict_list) == 100

def test_get_movie(in_memory_repo):
    a_movie_dict = services.get_movie("Guardians of the Galaxy", 2014, in_memory_repo)
    assert a_movie_dict["title"] == "Guardians of the Galaxy"
    assert a_movie_dict["release_year"] == 2014

def test_add_review(in_memory_repo):
    a_review_dict = services.add_review("thorke", "Guardians of the Galaxy", 2014, "Great Movie", 10, in_memory_repo)

    guardians_of_the_galaxy_movie = in_memory_repo.get_movie("Guardians of the Galaxy", 2014)

    review_in_review_list_bool = False
    for a_review in guardians_of_the_galaxy_movie.review_list:
        if a_review.review_text == "Great Movie" and a_review.user.user_name == "thorke": # assuming the rest are there
            review_in_review_list_bool = True
            break
    assert review_in_review_list_bool

def test_get_movies_with_actor_director_or_genre(in_memory_repo):
    # Chris Pratt is an actor in Guardians of the Galaxy
    # Ridley Scott directed Prometheus
    # Split is a Horror
    movie_dict_list = services.get_movies_with_actor_director_or_genre("Chris Pratt", "Ridley Scott", "Horror", in_memory_repo)
    
    movies_to_find_list = ["Guardians of the Galaxy", "Prometheus", "Split"]
    for movie_dict in movie_dict_list:
        movie_title = movie_dict["title"]
        if movie_title in movies_to_find_list:
            movies_to_find_list.pop(movies_to_find_list.index(movie_title))
    assert movies_to_find_list == []


def test_get_all_movies_with_database_repository(session_factory):
    database_repo = SqlAlchemyRepository(session_factory)

    assert len(services.get_all_movies(database_repo)) == 100
