from datetime import datetime

from sqlalchemy import select, inspect

from CS235Flix.adapters.orm import metadata


def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['actors', 'directors', 'genres', 'movie_actors', 'movie_genres', 'movies', 'reviews', 'users']


def test_database_populate_select_all_users(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[7]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_user_names = []
        for row in result:
            all_user_names.append(row['user_name'])

        assert ['thorke', 'fmercury', 'mjackson'] == all_user_names


def test_database_populate_select_all_reviews(database_engine): # checks all reviews (from review.csv - which is the test one) are there

    # Get table information
    inspector = inspect(database_engine)
    name_of_reviews_table = inspector.get_table_names()[6]

    with database_engine.connect() as connection:
        # query for records in table reviews
        select_statement = select([metadata.tables[name_of_reviews_table]])
        result = connection.execute(select_statement)

        all_reviews = []
        for row in result:
            all_reviews.append((row['id'], row['user_id'], row['movie_id'], row['review_text'], row['rating'], row['timestamp']))

        assert all_reviews == [(1, 1, 1, 'This was awesome!', 9.5, datetime(2020, 2, 23, 8, 12, 8)),
                                (2, 2, 1, 'Wow', 9.0, datetime(2020, 2, 24, 12, 52, 30))]


def test_database_populate_select_all_movies(database_engine): # checks the first one

    # Get table information
    inspector = inspect(database_engine)
    name_of_movies_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        # query for records in table articles
        select_statement = select([metadata.tables[name_of_movies_table]])
        result = connection.execute(select_statement)

        all_movies = []
        for row in result:
            all_movies.append((row['id'], row['title'], row['release_year'], row['description'], row['runtime_minutes'], row['external_rating'], row['external_rating_votes'], row['revenue'], row['metascore']))

        assert all_movies[0] == (1,
                                   'Guardians of the Galaxy',
                                   2014,
                                   'A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe.',
                                   121,
                                   8.1,
                                   757074,
                                   333.13,
                                   76)

def test_database_populate_selected_all_actors(database_engine): # checks Chris Pratt is in there

    # Get table information
    inspector = inspect(database_engine)
    name_of_actors_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        # query for records in table articles
        select_statement = select([metadata.tables[name_of_actors_table]])
        result = connection.execute(select_statement)

        all_actor_names = []
        for row in result:
            all_actor_names.append(row['actor_full_name'])


        assert "Chris Pratt" in all_actor_names

def test_database_populate_selected_all_directors(database_engine): # checks James Gunn is in there

    # Get table information
    inspector = inspect(database_engine)
    name_of_directors_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        # query for records in table articles
        select_statement = select([metadata.tables[name_of_directors_table]])
        result = connection.execute(select_statement)

        all_director_names = []
        for row in result:
            all_director_names.append(row['director_full_name'])

        #nr_articles = len(all_articles)

        assert "James Gunn" in all_director_names

def test_database_populate_selected_all_genres(database_engine): # checks Action and Horror is in there

    # Get table information
    inspector = inspect(database_engine)
    name_of_genres_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table articles
        select_statement = select([metadata.tables[name_of_genres_table]])
        result = connection.execute(select_statement)

        all_genre_names = []
        for row in result:
            all_genre_names.append(row['genre_name'])

        assert "Action" in all_genre_names and "Horror" in all_genre_names