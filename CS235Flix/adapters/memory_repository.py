import csv

import os
from datetime import datetime

from CS235Flix.adapters.movie_file_csv_reader import MovieFileCSVReader
from CS235Flix.adapters.repository import AbstractRepository

from CS235Flix.domain.movie import Movie, get_movie_hash
from CS235Flix.domain.director import Director
from CS235Flix.domain.actor import Actor
from CS235Flix.domain.person import get_person_hash
from CS235Flix.domain.genre import Genre, get_genre_hash

from CS235Flix.domain.user import User
from CS235Flix.domain.review import Review, make_review

from werkzeug.security import generate_password_hash

class MemoryRepository(AbstractRepository):
	def __init__(self):
		self.__movie_dict = dict()
		self.__director_dict = dict()
		self.__actor_dict = dict()
		self.__genre_dict = dict()
		self.__user_list = list()

	def add_movie(self, a_movie):
		self.__movie_dict[hash(a_movie)] = a_movie

	def get_movie(self, title, release_year):
		try:
			the_hash = get_movie_hash(title, release_year)
			return self.__movie_dict[the_hash]
		except KeyError:
			return None

	def get_all_movies(self):
		return list(self.__movie_dict.values())

	def add_director(self, a_director):
		self.__director_dict[hash(a_director)] = a_director

	def get_director(self, director_full_name):
		try:
			the_hash = get_person_hash(director_full_name)
			return self.__director_dict[the_hash]
		except KeyError:
			return None

	def get_all_directors(self):
		return list(self.__director_dict.values())

	def add_actor(self, a_actor):
		self.__actor_dict[hash(a_actor)] = a_actor

	def get_actor(self, actor_full_name):
		try:
			the_hash = get_person_hash(actor_full_name)
			return self.__actor_dict[the_hash]
		except KeyError:
			return None

	def get_all_actors(self):
		return list(self.__actor_dict.values())

	def add_genre(self, a_genre):
		self.__genre_dict[hash(a_genre)] = a_genre

	def get_genre(self, genre_name):
		try:
			the_hash = get_genre_hash(genre_name)
			return self.__genre_dict[the_hash]
		except KeyError:
			return None

	def get_all_genres(self):
		return list(self.__genre_dict.values())

	def add_user(self, user):
		self.__user_list.append(user)

	def get_user(self, user_name):
		return next((user for user in self.__user_list if user.user_name == user_name), None)

	def get_all_users(self):
		return self.__user_list

	def get_movies_with_actor(self, actor_full_name):
		movie_list = list()
		try:
			a_actor = self.get_actor(actor_full_name)
		except:
			return movie_list # Exception("Actor: {} is not in repository".format(actor_full_name))

		for a_movie in self.get_all_movies():
			if a_actor in a_movie.actors:
				movie_list.append(a_movie)
		return movie_list

	def get_movies_with_director(self, director_full_name):
		movie_list = list()
		try:
			a_director = self.get_director(director_full_name)
		except:
			#Exception("Director: {} is not in repository".format(director_full_name))
			return movie_list

		for a_movie in self.get_all_movies():
			if a_director == a_movie.director:
				movie_list.append(a_movie)
		return movie_list

	def get_movies_with_genre(self, genre_name):
		movie_list = list()
		try:
			a_genre = self.get_genre(genre_name)
		except:
			#Exception("Genre: {} is not in repository".format(genre_name))
			return movie_list

		for a_movie in self.get_all_movies():
			if a_genre in a_movie.genres:
				movie_list.append(a_movie)
		return movie_list

	def get_movies_with_actor_director_or_genre(self, actor_full_name, director_full_name, genre_name):
		movie_set_1 = set(self.get_movies_with_actor(actor_full_name))
		movie_set_2 = set(self.get_movies_with_director(director_full_name))
		movie_set_3 = set(self.get_movies_with_genre(genre_name))
		return movie_set_1.union(movie_set_2, movie_set_3)


def add_movies(a_repo_instance, movie_list):
	for a_movie in movie_list:
		a_repo_instance.add_movie(a_movie)

def add_directors(a_repo_instance, director_list):
	for a_director in director_list:
		a_repo_instance.add_director(a_director)

def add_actors(a_repo_instance, actor_list):
	for a_actor in actor_list:
		a_repo_instance.add_actor(a_actor)

def add_genres(a_repo_instance, genre_list):
	for a_genre in genre_list:
		a_repo_instance.add_genre(a_genre)

def add_users(a_repo_instance, user_list):
	for a_user in user_list:
		a_repo_instance.add_user(a_user)


def read_csv_file(csv_path): # a bit of magic
	with open(csv_path, encoding='utf-8-sig') as infile:
		reader = csv.reader(infile)

		# Read first line of the the CSV file.
		headers = next(reader)

		# Read remaining rows from the CSV file.
		for row in reader:
			# Strip any leading/trailing white space from data read.
			row = [item.strip() for item in row]
			yield row

def get_users_from_csv(user_csv_path):
	user_list = list()
	for data_row in read_csv_file(user_csv_path):
		user_name = data_row[1]
		password = data_row[2]
		hashed_password = generate_password_hash(password)
		a_user = User(user_name, hashed_password)
		user_list.append(a_user)
	return user_list

def create_reviews_from_csv_and_associate(review_csv_path, movie_list, user_list): # Note reviews don't exist standalone in the memory repository.
	# this just creates a review and associates it with movies/users from the memory repository
	for data_row in read_csv_file(review_csv_path):
		user_name = data_row[0]
		movie_title = data_row[1]
		movie_release_year = data_row[2]

		temp_movie = Movie(movie_title, int(movie_release_year))
		try:
			a_movie = movie_list[movie_list.index(temp_movie)]
		except:
			raise Exception("The movie: {} does not exist in the movie_list given, so a review has not been made".format(temp_movie, movie_list[:3]))

		temp_user = User(user_name, "doesn'tmatterwhatgoeshere")
		try:
			a_user = user_list[user_list.index(temp_user)]
		except:
			raise Exception("The user: {} does not exist in the movie_list given, so a review has not been made".format(user_name))

		review_text = data_row[3]
		rating = float(data_row[4])
		timestamp = datetime.fromisoformat(data_row[5])

		make_review(a_user, a_movie, review_text, rating, timestamp) # this function is always called to store the review in both the user and movie


def populate(data_path, a_repo_instance):
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

	add_movies(a_repo_instance, movie_list)
	add_directors(a_repo_instance, director_list)
	add_actors(a_repo_instance, actor_list)
	add_genres(a_repo_instance, genre_list)
	add_users(a_repo_instance, user_list)



