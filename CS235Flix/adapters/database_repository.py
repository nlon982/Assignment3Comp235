import os

from CS235Flix.adapters.memory_repository import create_reviews_from_csv_and_associate, get_users_from_csv
from CS235Flix.adapters.movie_file_csv_reader import MovieFileCSVReader

from sqlalchemy import desc, asc
from sqlalchemy.engine import Engine
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from werkzeug.security import generate_password_hash

from sqlalchemy.orm import scoped_session, sessionmaker
from flask import _app_ctx_stack

from CS235Flix.adapters.repository import AbstractRepository

from CS235Flix.domain.movie import Movie
from CS235Flix.domain.director import Director
from CS235Flix.domain.actor import Actor
from CS235Flix.domain.genre import Genre
from CS235Flix.domain.user import User
from CS235Flix.domain.review import Review


class SessionContextManager:
	def __init__(self, session_factory):
		self.__session_factory = session_factory
		self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

	def __enter__(self):
		return self

	def __exit__(self, *args):
		self.rollback()

	@property
	def session(self):
		return self.__session

	def commit(self):
		self.__session.commit()

	def rollback(self):
		self.__session.rollback()

	def reset_session(self):
		# this method can be used e.g. to allow Flask to start a new session for each http request,
		# via the 'before_request' callback
		self.close_current_session()
		self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

	def close_current_session(self):
		if not self.__session is None:
			self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

	def __init__(self, session_factory):
		self._session_cm = SessionContextManager(session_factory)

	def close_session(self):
		self._session_cm.close_current_session()

	def reset_session(self):
		self._session_cm.reset_session()

	def add_movie(self, a_movie):
		with self._session_cm as scm:
			scm.session.add(a_movie)
			scm.commit()

	def get_movie(self, title, release_year):
		a_movie = None
		try:
			a_movie = self._session_cm.session.query(Movie).filter_by(_Movie__title = title, _Movie__release_year = release_year).one()
		except NoResultFound:
			pass
		return a_movie

	def get_all_movies(self):
		movie_list = list()
		try:
			movie_list = self._session_cm.session.query(Movie).all()
		except NoResultFound:
			pass
		return movie_list

	def add_director(self, a_director):
		with self._session_cm as scm:
			scm.session.add(a_director)
			scm.commit()

	def get_director(self, director_full_name):
		a_director = None
		try:
			a_director = self._session_cm.session.query(Director).filter_by(_Person__full_name = director_full_name).one()
		except NoResultFound:
			pass
		return a_director

	def get_all_directors(self):
		director_list = list()
		try:
			director_list = self._session_cm.session.query(Director).all()
		except:
			pass
		return director_list

	def add_actor(self, a_actor):
		with self._session_cm as scm:
			scm.session.add(a_actor)
			scm.commit()

	def get_actor(self, actor_full_name):
		a_actor = None
		try:
			a_actor = self._session_cm.session.query(Actor).filter_by(_Person__full_name = actor_full_name).one()
		except NoResultFound:
			pass
		return a_actor

	def get_all_actors(self):
		actor_list = list()
		try:
			actor_list = self._session_cm.session.query(Actor).all()
		except:
			pass
		return actor_list

	def add_genre(self, a_genre):
		with self._session_cm as scm:
			scm.session.add(a_genre)
			scm.commit()

	def get_genre(self, genre_name):
		a_genre = None
		try:
			a_genre = self._session_cm.session.query(Genre).filter_by(_Genre__genre_name = genre_name).one()
		except NoResultFound:
			pass
		return a_genre

	def get_all_genres(self):
		genre_list = list()
		try:
			genre_list = self._session_cm.session.query(Genre).all()
		except:
			pass
		return genre_list

	def add_user(self, a_user):
		with self._session_cm as scm:
			scm.session.add(a_user)
			scm.commit()

	def get_user(self, user_name):
		a_user = None
		try:
			a_user = self._session_cm.session.query(User).filter_by(_User__user_name = user_name).one()
		except NoResultFound:
			pass
		return a_user

	def get_all_users(self):
		user_list = list()
		try:
			user_list = self._session_cm.session.query(User).all()
		except:
			pass
		return user_list

	def get_movies_with_actor(self, actor_full_name):
		movie_id_list = []

		# Use native SQL to retrieve article ids, since there is no mapped class for the article_tags table.
		row = self._session_cm.session.execute('SELECT id FROM actors WHERE actor_full_name = :actor_full_name', {'actor_full_name': actor_full_name}).fetchone()

		if row is None:
			# No actors with actor_full_name
			pass
		else:
			actor_id = row[0] # they'll only be one of that actor in the database (because of uniqueness, and that's how we intended it)

			# Retrieve article ids of articles associated with the tag.
			movie_id_list = self._session_cm.session.execute('SELECT movie_id FROM movie_actors WHERE actor_id = {}'.format(actor_id)).fetchall() # .format suffices (because not a multiple word string?)
			movie_id_list = [id[0] for id in movie_id_list]

		movie_list = self._session_cm.session.query(Movie).filter(Movie.id.in_(movie_id_list)).all()
		return movie_list

	def get_movies_with_director(self, director_full_name):
		movie_id_list = []

		# Use native SQL to retrieve article ids, since there is no mapped class for the article_tags table.
		row = self._session_cm.session.execute('SELECT id FROM directors WHERE director_full_name = :director_full_name', {'director_full_name': director_full_name}).fetchone()

		if row is None:
			# no directors with director_full_name
			pass
		else:
			director_id = row[0]

			# Retrieve article ids of articles associated director.
			movie_id_list = self._session_cm.session.execute('SELECT id FROM movies WHERE director_id = {}'.format(director_id)).fetchall() # recall director_id is a foreign key, using director.id
			movie_id_list = [id[0] for id in movie_id_list]

		movie_list = self._session_cm.session.query(Movie).filter(Movie.id.in_(movie_id_list)).all()
		return movie_list

	def get_movies_with_genre(self, genre_name):
		movie_id_list = []

		# Use native SQL to retrieve article ids, since there is no mapped class for the article_tags table.
		row = self._session_cm.session.execute('SELECT id FROM genres WHERE genre_name = :genre_name', {'genre_name': genre_name}).fetchone()

		if row is None:
			# No genres with genre_name
			pass
		else:
			genre_id = row[0]

			# Retrieve article ids of articles associated with the tag.
			movie_id_list = self._session_cm.session.execute('SELECT movie_id FROM movie_genres WHERE genre_id = {}'.format(genre_id)).fetchall()
			movie_id_list = [id[0] for id in movie_id_list]

		movie_list = self._session_cm.session.query(Movie).filter(Movie.id.in_(movie_id_list)).all()
		return movie_list

	def get_movies_with_actor_director_or_genre(self, actor_full_name, director_full_name, genre_name): # the key word is "or", as in, it takes the union of movies it finds with this actor, director and genre
		# this could almost be implemented in the AbstractRepository class, as it's implementation is identical to memory_repository (and any other child class i'll make)
		movie_set_1 = set(self.get_movies_with_actor(actor_full_name))
		movie_set_2 = set(self.get_movies_with_director(director_full_name))
		movie_set_3 = set(self.get_movies_with_genre(genre_name))
		return movie_set_1.union(movie_set_2, movie_set_3)


def populate(engine, data_path):
	movie_csv_path = os.path.join(data_path, 'Data1000Movies.csv')
	user_csv_path = os.path.join(data_path, 'users.csv')
	review_csv_path = os.path.join(data_path, 'reviews.csv')

	movie_file_csv_reader_object = MovieFileCSVReader(movie_csv_path)
	movie_file_csv_reader_object.read_csv_file()

	movie_list = movie_file_csv_reader_object.dataset_of_movies
	director_list = movie_file_csv_reader_object.dataset_of_directors
	actor_list = movie_file_csv_reader_object.dataset_of_actors
	genre_list = movie_file_csv_reader_object.dataset_of_genres
	user_list = get_users_from_csv(user_csv_path)

	create_reviews_from_csv_and_associate(review_csv_path, movie_list, user_list)

	# movie objects stores actor, genre & review objects.
	# so the ORM only needs movie objects & user objects to have everything

	session_factory = sessionmaker(autocommit = False, autoflush = True, bind = engine)

	session = session_factory()

	for a_movie in movie_list:
		session.add(a_movie)

	for a_director in director_list:
		session.add(a_director)

	for a_actor in actor_list:
		session.add(a_actor)

	for a_genre in genre_list:
		session.add(a_genre)

	for a_user in user_list:
		session.add(a_user)

	session.commit()