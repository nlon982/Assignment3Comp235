from sqlalchemy import (
    Table, MetaData, Column, Integer, Float, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from CS235Flix.domain.movie import Movie
from CS235Flix.domain.director import Director
from CS235Flix.domain.actor import Actor
from CS235Flix.domain.genre import Genre
from CS235Flix.domain.user import User
from CS235Flix.domain.review import Review

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key = True, autoincrement = True),
    Column('user_name', String(255), unique = True, nullable = False),
    Column('password', String(255), nullable = False),
    Column('time_spent_watching_movies', Integer, nullable = True)
)
# left out watched_movies (this would go in the mapper though, right?)

reviews = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key = True, autoincrement = True),
    Column('user_id', ForeignKey('users.id')),
    Column('movie_id', ForeignKey('movies.id')),
    Column('review_text', String(1024), nullable = False),
    Column('rating', Float, nullable = True),
    Column('timestamp', DateTime, nullable = False)
)

movies = Table(
    'movies', metadata,
    Column('id', Integer, primary_key = True, autoincrement = True),
    Column('title', String(255), nullable = True),
    Column('release_year', Integer, nullable = True),
    Column('description', String(1024), nullable = True),
    Column('director_id', ForeignKey('directors.id')),
    Column('runtime_minutes', Integer, nullable = True),
    Column('external_rating', Float, nullable = True),
    Column('external_rating_votes', Integer, nullable = True),
    Column('revenue', Float, nullable = True),
    Column('metascore', Integer, nullable = True),
)

actors = Table(
    'actors', metadata,
    Column('id', Integer, primary_key = True, autoincrement = True),
    Column('actor_full_name', String(255), unique = True, nullable = True)
)

directors = Table(
    'directors', metadata,
    Column('id', Integer, primary_key = True, autoincrement = True),
    Column('director_full_name', String(255), unique = True, nullable = True)
)
genres = Table(
    'genres', metadata,
    Column('id', Integer, primary_key = True, autoincrement = True),
    Column('genre_name', String(255), unique = True, nullable = True)
)

movie_actors = Table(
    'movie_actors', metadata,
    Column('id', Integer, primary_key = True, autoincrement = True),
    Column('movie_id', ForeignKey('movies.id')),
    Column('actor_id', ForeignKey('actors.id'))
)

movie_genres = Table(
    'movie_genres', metadata,
    Column('id', Integer, primary_key = True, autoincrement = True),
    Column('movie_id', ForeignKey('movies.id')),
    Column('genre_id', ForeignKey('genres.id'))
)

def map_model_to_tables():
    mapper(User, users, properties = {
        '_User__user_name': users.c.user_name,
        '_User__password': users.c.password,
        '_User__time_spent_watching_movies': users.c.time_spent_watching_movies,
        '_User__reviews': relationship(Review, backref = '_Review__user')
    })
    mapper(Review, reviews, properties = {
        '_Review__review_text': reviews.c.review_text,
        '_Review__rating': reviews.c.rating,
        '_Review__timestamp': reviews.c.timestamp
    })

    actors_mapper = mapper(Actor, actors, properties = {
        '_Person__full_name': actors.c.actor_full_name,
    })
    directors_mapper = mapper(Director, directors, properties = {
        '_Person__full_name': directors.c.director_full_name,
    })
    genres_mapper = mapper(Genre, genres, properties = {
        '_Genre__genre_name': genres.c.genre_name
    })

    mapper(Movie, movies, properties = {
        '_Movie__title': movies.c.title,
        '_Movie__release_year': movies.c.release_year,
        '_Movie__description': movies.c.description,
        '_Movie__runtime_minutes': movies.c.runtime_minutes,
        '_Movie__external_rating': movies.c.external_rating,
        '_Movie__external_rating_votes': movies.c.external_rating_votes,
        '_Movie__revenue': movies.c.revenue,
        '_Movie__metascore': movies.c.metascore,
        '_Movie__review_list': relationship(Review, backref = '_Review__movie'),
        '_Movie__director': relationship(Director),
        '_Movie__actors': relationship(
            actors_mapper,
            secondary = movie_actors,
            backref = "_movies"
        ),
        '_Movie__genres': relationship(
            genres_mapper,
            secondary = movie_genres,
            backref = "_movies"
        ),
    })

