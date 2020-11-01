import os
import pytest

from CS235Flix.adapters.database_repository import SqlAlchemyRepository

from CS235Flix.adapters.memory_repository import MemoryRepository, populate
from CS235Flix.domain.movie import Movie
from CS235Flix.domain.user import User
from CS235Flix.domain.actor import Actor
from CS235Flix.domain.director import Director
from CS235Flix.domain.genre import Genre

from CS235Flix.domain.review import Review, make_review


class TestsDatabaseRepositoryWithData: # this inherently tests getters and setters for movies, directors, actors and genres
    def test_get_movie(self, session_factory):
        database_repo = SqlAlchemyRepository(session_factory)
        
        assert isinstance(database_repo.get_movie("Guardians of the Galaxy", 2014), Movie)

    def test_get_director(self, session_factory): # tests
        database_repo = SqlAlchemyRepository(session_factory)
        
        assert isinstance(database_repo.get_director("James Gunn"), Director)

    def test_get_actor(self, session_factory):
        database_repo = SqlAlchemyRepository(session_factory)
        
        assert isinstance(database_repo.get_actor("Chris Pratt"), Actor)

    def test_get_genre(self, session_factory):
        database_repo = SqlAlchemyRepository(session_factory)
        
        assert isinstance(database_repo.get_genre("Action"), Genre)

    def test_get_user(self, session_factory): # inherently means it loaded in the users.csv correctly
        database_repo = SqlAlchemyRepository(session_factory)
        
        assert isinstance(database_repo.get_user("thorke"), User)

    def test_get_all(self, session_factory): # not much to test without knowing how many of each there are
        database_repo = SqlAlchemyRepository(session_factory)
        
        assert isinstance(database_repo.get_all_movies(), list)
        assert isinstance(database_repo.get_all_directors(), list)
        assert isinstance(database_repo.get_all_actors(), list)
        assert isinstance(database_repo.get_all_genres(), list)
        assert isinstance(database_repo.get_all_users(), list)

    def test_get_nonexistent_movie(self, session_factory):
        database_repo = SqlAlchemyRepository(session_factory)
        
        assert database_repo.get_movie("sdjksjkdas", 2014) == None

    def test_get_nonexistent_director(self, session_factory):
        database_repo = SqlAlchemyRepository(session_factory)
        
        assert database_repo.get_director("sdjksjkdas") == None

    def test_get_nonexistent_actor(self, session_factory):
        database_repo = SqlAlchemyRepository(session_factory)
        
        assert database_repo.get_actor("sdjksjkdas") == None

    def test_get_nonexistent_genre(self, session_factory):
        database_repo = SqlAlchemyRepository(session_factory)
        
        assert database_repo.get_genre("sdjksjkdas") == None

    def test_get_nonexistent_user(self, session_factory):
        database_repo = SqlAlchemyRepository(session_factory)
        
        assert database_repo.get_user("sdjksjkdas") == None

    def test_get_movies_with_actor(self, session_factory): # assumes get_movie works
        database_repo = SqlAlchemyRepository(session_factory)
        
        assert database_repo.get_movie("Guardians of the Galaxy", 2014) in database_repo.get_movies_with_actor("Chris Pratt")

    def test_get_movies_with_director(self, session_factory): # assumes get_movie works
        database_repo = SqlAlchemyRepository(session_factory)
        
        assert database_repo.get_movie("Guardians of the Galaxy", 2014) in database_repo.get_movies_with_director("James Gunn")

    def test_get_movies_with_genre(self, session_factory): # assumes get_movie works
        database_repo = SqlAlchemyRepository(session_factory)
        
        assert database_repo.get_movie("Guardians of the Galaxy", 2014) in database_repo.get_movies_with_genre("Action")

    def test_get_movies_with_actor_director_or_genre(self, session_factory): # assumes get_movie works
        database_repo = SqlAlchemyRepository(session_factory)
        
        movie_list = database_repo.get_movies_with_actor_director_or_genre("Chris Pratt", "M. Night Shyamalan", "Adventure")
        assert database_repo.get_movie("Guardians of the Galaxy", 2014) in movie_list
        assert database_repo.get_movie("Prometheus", 2012) in movie_list
        assert database_repo.get_movie("Split", 2016) in movie_list

    def test_loaded_in_reviews_csv(self, session_factory):
        database_repo = SqlAlchemyRepository(session_factory)
        
        a_movie = database_repo.get_movie("Guardians of the Galaxy", 2014)
        assert len(a_movie.review_list) == 2

    def test_loaded_in_users_csv(self, session_factory):
        database_repo = SqlAlchemyRepository(session_factory)
        
        assert len(database_repo.get_all_users()) == 3


class TestsBlankDatabaseRepository: # just in case
    def test_add_and_get_movie(self, blank_session_factory):
        database_repo = SqlAlchemyRepository(blank_session_factory)
        
        a_movie = Movie("Step Brothers", 2004)
        database_repo.add_movie(a_movie)
        assert a_movie in database_repo.get_all_movies()

    def test_add_and_get_director(self, blank_session_factory):
        database_repo = SqlAlchemyRepository(blank_session_factory)
        
        a_director = Director("Ted Jones")
        database_repo.add_director(a_director)
        assert a_director in database_repo.get_all_directors()

    def test_add_and_get_actor(self, blank_session_factory):
        database_repo = SqlAlchemyRepository(blank_session_factory)
        
        a_actor = Actor("Betty White")
        database_repo.add_actor(a_actor)
        assert a_actor in database_repo.get_all_actors()

    def test_add_and_get_genre(self, blank_session_factory):
        database_repo = SqlAlchemyRepository(blank_session_factory)
        
        a_genre = Genre("Thriller")
        database_repo.add_genre(a_genre)
        assert a_genre in database_repo.get_all_genres()

    def test_add_and_get_user(self, blank_session_factory):
        database_repo = SqlAlchemyRepository(blank_session_factory)
        
        a_user = User("oldmanjenkins", "Elephant12")
        database_repo.add_user(a_user)
        assert a_user in database_repo.get_all_users()