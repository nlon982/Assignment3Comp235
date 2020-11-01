import pytest

from CS235Flix.domain.director import Director
from CS235Flix.domain.genre import Genre
from CS235Flix.domain.actor import Actor
from CS235Flix.domain.movie import Movie
from CS235Flix.domain.review import Review
from CS235Flix.domain.user import User
from CS235Flix.domain.watchlist import WatchList


class TestDirectorMethods: # could make a fixture for each of the directors to stop repeated code
    def test_init_and_repr(self):
        director1 = Director("Taika Waititi")
        assert repr(director1) == "<Director Taika Waititi>"
        director2 = Director("")
        assert director2.director_full_name is None
        director3 = Director(42)
        assert director3.director_full_name is None

    def test_eq(self):
        director1 = Director("Taika Waititi")
        director2 = Director("Ben Zebra")
        director3 = Director("Taika Waititi")

        assert (director1 == director3) == True
        assert (director1 == director2) == False # Yes, I know I could do !=

    def test_lt(self):
        director1 = Director("Taika Waititi")
        director2 = Director("Ben Zebra")
        assert (director2 < director1) == True # expect Ben to be less than Taika

    def test_hash(self):
        director1 = Director("Taika Waititi")
        director2 = Director("Ben Zebra")
        assert (hash(director1) == hash(director2)) == False # two hashes ?shouldn't? be the same


class TestGenreMethods: # could make fixtures to stop repeated code
    def test_init_and_repr(self):
        genre1 = Genre("Horror")
        assert repr(genre1) == "<Genre Horror>"
        genre2 = Genre("")
        assert genre2.genre_name is None
        genre3 = Genre(42)
        assert genre3.genre_name is None


    def test_eq(self):
        genre1 = Genre("Horror")
        genre2 = Genre("Comedy")
        genre3 = Genre("Horror")
        assert (genre1 == genre3) == True
        assert (genre1 == genre2) == False  # Yes, I know I could do != with True


    def test_lt(self):
        genre1 = Genre("Horror")
        genre2 = Genre("Comedy")
        assert (genre2 < genre1) == True  # expect Comedy to be less than Horror


    def test_hash(self):
        genre1 = Genre("Horror")
        genre2 = Genre("Comedy")
        genre3 = Genre("Horror")
        assert (hash(genre1) == hash(genre2)) == False  # two hashes ?shouldn't? be the same
        assert (hash(genre1) == hash(genre3)) == True  # hash should be the same since same genre_name (that's what hash is based on_


class TestActorMethods: # could make a fixture for each of the directors to stop repeated code
    def test_init_and_repr(self):
        actor1 = Actor("Tom Cruise")
        assert repr(actor1) == "<Actor Tom Cruise>"
        actor2 = Actor("")
        assert actor2.actor_full_name is None
        actor3 = Actor(42)
        assert actor3.actor_full_name is None

    def test_eq(self):
        actor1 = Actor("Tom Cruise")
        actor2 = Actor("Dwayne Johnson")
        actor3 = Actor("Tom Cruise")

        assert (actor1 == actor3) == True
        assert (actor1 == actor2) == False # Yes, I know I could do !=

    def test_lt(self):
        actor1 = Actor("Tom Cruise")
        actor2 = Actor("Dwayne Johnson")
        assert (actor2 < actor1) == True # expect Dwayne to be less than Taika

    def test_hash(self):
        actor1 = Actor("Tom Cruise")
        actor2 = Actor("Dwayne Johnson")
        actor3 = Actor("Tom Cruise")
        assert (hash(actor1) == hash(actor2)) == False # two hashes ?shouldn't? be the same
        assert (hash(actor1) == hash(actor3)) == True  # same name, so should have same hash (that's how this hash is decided)

    def test_add_actor_colleague(self):
        actor1 = Actor("Tom Cruise")
        colleague1 = Actor("Dwayne Johnson")

        actor1.add_actor_colleague(colleague1)
        assert actor1.check_if_this_actor_worked_with(colleague1) == True

class TestMovieMethods:
    def test_init_and_getters_work(self): # i.e. this inherently test the getters (via @property) work too
        a_movie = Movie("Back To The Future", 1965)
        assert a_movie.title == "Back To The Future"
        assert a_movie.release_year == 1965

        # again, these tests have to be repeated with the setters because init has the code too
        a_movie_two = Movie("", 1965)
        a_movie_three = Movie(4, 1965)
        assert (a_movie_two.title == None) and (a_movie_three.title == None)
        a_movie_four = Movie("Back To The Future", 1865)
        assert(a_movie_four.release_year == None)

        assert a_movie.release_year == 1965
        assert a_movie.description == None
        assert a_movie.director == None
        assert len(a_movie.actors) == 0
        assert len(a_movie.genres) == 0
        assert a_movie.runtime_minutes == None


        # more (not required)
        #assert a_movie.external_rating == None
        #assert a_movie.external_rating_votes == None
        #assert a_movie.revenue == None
        #assert a_movie.metascore == None


    def test_setters(self): # inherently tests getters too
        a_movie = Movie("Back To The Future", 1965)
        director1 = Director("Brad Bird")

        a_movie.title = "  Mission Impossible: Ghost Protocol  "
        assert a_movie.title == "Mission Impossible: Ghost Protocol"
        a_movie.title = 15
        #assert a_movie.title == "Mission Impossible: Ghost Protocol"

        a_movie.description = "  An action movie  "
        assert a_movie.description == "An action movie"

        a_movie.director = director1
        assert a_movie.director == director1

        actor1 = Actor("Tom Cruise")
        actor2 = Actor("Simon Pegg")
        a_movie.actors = [actor1, actor2]
        assert a_movie.actors == [actor1, actor2]

        genre1 = Genre("Action")
        genre2 = Genre("Comedy")
        a_movie.genres = [genre1, genre2]
        assert a_movie.genres == [genre1, genre2]

        a_movie.runtime_minutes = 100
        assert a_movie.runtime_minutes == 100
        assert type(a_movie.runtime_minutes) == int
        with pytest.raises(ValueError):
            a_movie.runtime_minutes = 0
            a_movie.runtime_minutes = -10

    def test_special_methods(self):
        a_movie = Movie("Back To The Future", 1965)
        a_movie_two = Movie("Back To The Future", 1965)
        a_movie_three = Movie("Back To The Future", 1969)
        a_movie_four = Movie("A Quiet Place", 2018)

        assert a_movie == a_movie_two # according to the "domain model" these two are equivelant. so yep.

        assert a_movie_four < a_movie # testing that it sorts by titles (if not same)
        assert a_movie < a_movie_three # testing that it sorts by year if titles same

        assert hash(a_movie) != hash(a_movie_three) # checking that hash is influenced by year and title (if these hashes are indeed not equal, mission accomplished)

        # a practical use of hash
        #a_dict = dict()
        #a_dict[a_movie] = "a_movie"
        #a_dict[a_movie_two] = "a_movie_two"
        #a_dict[a_movie_three] = "a_movie_three"
        #assert a_dict[a_movie]  == a_dict[a_movie_two] # these are the same move name and year, so should be the same hash, and thus the same dict key




        assert repr(a_movie) == "<Movie Back To The Future, 1965>"

    def test_more_methods(self):
        a_movie = Movie("Back To The Future", 1965)
        actor1 = Actor("Michael J. Fox")
        actor2 = Actor("Christopher Lloyd")
        genre1 = Genre("Horror")
        genre2 = Genre("Comedy")

        a_movie.add_actor(actor1)
        assert a_movie.actors == [actor1]
        a_movie.add_actor(actor1)
        assert a_movie.actors == [actor1] # test it doesn't add duplicate actors
        a_movie.add_actor(actor2)
        assert a_movie.actors == [actor1, actor2] # tests actors are added (and in order, not that it matters)

        a_movie.remove_actor(actor1)
        assert a_movie.actors == [actor2]
        a_movie.remove_actor(5) # test it doesn't throw an error if not an actor
        assert a_movie.actors == [actor2] # test it doesn't randomly remove an actor (I don't see how but yeah)


        a_movie.add_genre(genre1)
        assert a_movie.genres == [genre1]
        a_movie.add_genre(genre1)
        assert a_movie.genres == [genre1] # test it doesn't add duplicate actors
        a_movie.add_genre(genre2)
        assert a_movie.genres == [genre1, genre2]  # tests actors are added (and in order, not that it matters)

        a_movie.remove_genre(genre1)
        assert a_movie.genres == [genre2]
        a_movie.remove_genre(5)  # test it doesn't throw an error if not a genre
        assert a_movie.genres == [genre2]  # test it doesn't randomly remove an genre (I don't see how but yeah)


class TestReview:
    def test_init(self):
        review = Review(User("BobBoilen", "Elephant12"), Movie("Star Wars", 1999), "Great Movie", 10)

        assert review.movie.title == "Star Wars"
        assert review.review_text == "Great Movie"
        assert review.rating == 10
        assert review.user.user_name == "bobboilen"
        #assert repr(review) == "<Review Star Wars 1999, Great Movie, 10 (4-9-2020)>" # dependent on date

class TestUser:
    def test_all(self):
        user1 = User("nathanl127", "passwordgoeshere")
        user2 = User("boomer127", "passwordgoeshere")
        review = Review(user1, Movie("Star Wars", 1999), "Great Movie", 10)
        a_movie = Movie("Back To The Future", 1965)
        a_movie.runtime_minutes = 10

        assert user1.user_name == "nathanl127"
        assert user1.password == "passwordgoeshere"
        assert user1.reviews == []
        assert user1.time_spent_watching_movies_minutes == 0
        assert len(user1.watched_movies) == 0

        user1.watch_movie(a_movie)
        assert len(user1.watched_movies) == 1
        assert user1.time_spent_watching_movies_minutes == 10

        user1.add_review(review)
        assert len(user1.reviews) == 1

        assert repr(user1) == "<User nathanl127>"
        assert user2 < user1
        assert hash(user1) != hash(user2)


class TestWatchList: # haven't implemented, but here are the test cases
    def test_init_and_size(self):
        watchlist = WatchList()
        assert watchlist.size() == 0 # check starts with 0 movies in watchlist (assumes size works)

    def test_add_movie(self):
        watchlist = WatchList()
        watchlist.add_movie(Movie("Star Wars", 1999))
        assert watchlist.size() == 1 # tests that add and size are working..
        watchlist.add_movie(Movie("Star Wars", 1999))
        assert watchlist.size() == 1 # test that indeed a duplicate movie can't be added

    def test_remove_movie(self):
        watchlist = WatchList()
        movie1 = Movie("Star Wars", 1999)
        watchlist.add_movie(movie1)
        assert watchlist.size() == 1
        watchlist.remove_movie(movie1)
        assert watchlist.size() == 0 # tests it removes a movie if it is there
        watchlist.remove_movie(movie1)
        assert watchlist.size() == 0 # tests it does nothing if movie not there

    def test_select_movie_to_watch(self):
        watchlist = WatchList()
        movie1 = Movie("Moana", 2016)
        movie2 = Movie("Ice Age", 2002)
        movie3 = Movie("Guardians of the Galaxy", 2012)
        watchlist.add_movie(movie1)
        watchlist.add_movie(movie2)
        watchlist.add_movie(movie3)

        assert watchlist.select_movie_to_watch(0) == movie1
        # ^ note: could've just done "== Movie("Moana", 2016)" since __eq__ is defined by same title and year
        assert watchlist.select_movie_to_watch(1) == movie2
        assert watchlist.select_movie_to_watch(3) == None # tests that it gives None if range out of bounds

    def test_size(self): # this test is a bit silly since most the other tests rely on size working?
        watchlist = WatchList()
        assert watchlist.size() == 0
        watchlist.remove_movie(Movie("Star Wars", 1999))
        assert watchlist.size() == 0
        # ^ I believe this is a great test, checking that remove_movie
        # doesn't subtract 1 from size unless a movie is indeed removed

        watchlist.add_movie(Movie("Star Wars", 1999))
        assert watchlist.size() == 1
        watchlist.add_movie(Movie("Ice Age", 2002))
        assert watchlist.size() == 2
        watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
        assert watchlist.size() == 3
        watchlist.remove_movie(Movie("Star Wars", 1999))
        # ^ as per note above note, __eq___ is defined by same title and year, so this should do the job of removing
        assert watchlist.size() == 2 # test size reacts to movies being removed


    def test_first_movie_in_watchlist(self):
        watchlist = WatchList()
        movie1 = Movie("Moana", 2016)
        watchlist.add_movie(Movie("Moana", 2016))
        watchlist.add_movie(Movie("Ice Age", 2002))
        watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
        assert watchlist.first_movie_in_watchlist() == movie1


    def test_iterable(self):
        # note, a for loop uses '__iter__' (and '__next__' on the iterable object returned from __iter__)
        # so checking a for loop works, and correctly, is sufficient
        watchlist = WatchList()

        movie1 = Movie("Moana", 2016)
        movie2 = Movie("Ice Age", 2002)
        movie3 = Movie("Guardians of the Galaxy", 2012)
        watchlist.add_movie(movie1)
        watchlist.add_movie(movie2)
        watchlist.add_movie(movie3)

        # one way to do it
        a_list = [movie1, movie2, movie3]
        index = 0
        for movie in watchlist:
            assert movie == a_list[index]
            index += 1




