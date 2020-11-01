import os

import pytest

from CS235Flix.adapters.memory_repository import MemoryRepository, populate
from CS235Flix.domain.movie import Movie
from CS235Flix.domain.user import User
from CS235Flix.domain.actor import Actor
from CS235Flix.domain.director import Director
from CS235Flix.domain.genre import Genre

from CS235Flix.domain.review import Review, make_review

class TestsMemoryRepositoryWithData: # this inherently tests getters and setters for movies, directors, actors and genres
    def test_get_movie(self, in_memory_repo):
        assert isinstance(in_memory_repo.get_movie("Guardians of the Galaxy", 2014), Movie)

    def test_get_director(self, in_memory_repo): # tests
        assert isinstance(in_memory_repo.get_director("James Gunn"), Director)

    def test_get_actor(self, in_memory_repo):
        assert isinstance(in_memory_repo.get_actor("Chris Pratt"), Actor)

    def test_get_genre(self, in_memory_repo):
        assert isinstance(in_memory_repo.get_genre("Action"), Genre)

    def test_get_user(self, in_memory_repo): # inherently means it loaded in the users.csv correctly
        assert isinstance(in_memory_repo.get_user("thorke"), User)

    def test_get_all(self, in_memory_repo): # not much to test without knowing how many of each there are
        assert isinstance(in_memory_repo.get_all_movies(), list)
        assert isinstance(in_memory_repo.get_all_directors(), list)
        assert isinstance(in_memory_repo.get_all_actors(), list)
        assert isinstance(in_memory_repo.get_all_genres(), list)
        assert isinstance(in_memory_repo.get_all_users(), list)

    def test_get_nonexistent_movie(self, in_memory_repo):
        assert in_memory_repo.get_movie("sdjksjkdas", 2014) == None

    def test_get_nonexistent_director(self, in_memory_repo):
        assert in_memory_repo.get_director("sdjksjkdas") == None

    def test_get_nonexistent_actor(self, in_memory_repo):
        assert in_memory_repo.get_actor("sdjksjkdas") == None

    def test_get_nonexistent_genre(self, in_memory_repo):
        assert in_memory_repo.get_genre("sdjksjkdas") == None

    def test_get_nonexistent_user(self, in_memory_repo):
        assert in_memory_repo.get_user("sdjksjkdas") == None

    def test_get_movies_with_actor(self, in_memory_repo):
        assert in_memory_repo.get_movie("Guardians of the Galaxy", 2014) in in_memory_repo.get_movies_with_actor("Chris Pratt")

    def test_get_movies_with_director(self, in_memory_repo):
        assert in_memory_repo.get_movie("Guardians of the Galaxy", 2014) in in_memory_repo.get_movies_with_director("James Gunn")

    def test_get_movies_with_genre(self, in_memory_repo):
        assert in_memory_repo.get_movie("Guardians of the Galaxy", 2014) in in_memory_repo.get_movies_with_genre("Action")

    def test_get_movies_with_actor_director_or_genre(self, in_memory_repo):
        movie_list = in_memory_repo.get_movies_with_actor_director_or_genre("Chris Pratt", "M. Night Shyamalan", "Adventure")
        assert in_memory_repo.get_movie("Guardians of the Galaxy", 2014) in movie_list
        assert in_memory_repo.get_movie("Prometheus", 2012) in movie_list
        assert in_memory_repo.get_movie("Split", 2016) in movie_list

    def test_loaded_in_reviews_csv(self, in_memory_repo):
        a_movie = in_memory_repo.get_movie("Guardians of the Galaxy", 2014)
        assert len(a_movie.review_list) == 2

    def test_loaded_in_users_csv(self, in_memory_repo):
        assert len(in_memory_repo.get_all_users()) == 3


class TestsBlankMemoryRepository: # just in case
    def test_add_and_get_movie(self, blank_memory_repository):
        a_movie = Movie("Step Brothers", 2004)
        blank_memory_repository.add_movie(a_movie)
        assert a_movie in blank_memory_repository.get_all_movies()

    def test_add_and_get_director(self, blank_memory_repository):
        a_director = Director("Ted Jones")
        blank_memory_repository.add_director(a_director)
        assert a_director in blank_memory_repository.get_all_directors()

    def test_add_and_get_actor(self, blank_memory_repository):
        a_actor = Actor("Betty White")
        blank_memory_repository.add_actor(a_actor)
        assert a_actor in blank_memory_repository.get_all_actors()

    def test_add_and_get_genre(self, blank_memory_repository):
        a_genre = Genre("Thriller")
        blank_memory_repository.add_genre(a_genre)
        assert a_genre in blank_memory_repository.get_all_genres()

    def test_add_and_get_user(self, blank_memory_repository):
        a_user = User("oldmanjenkins", "Elephant12")
        blank_memory_repository.add_user(a_user)
        assert a_user in blank_memory_repository.get_all_users()