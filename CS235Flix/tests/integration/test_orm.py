import pytest

import datetime

from sqlalchemy.exc import IntegrityError

from CS235Flix.domain.movie import Movie
from CS235Flix.domain.review import make_review
from CS235Flix.domain.user import User

movie_date = datetime.date(2020, 2, 28)

def insert_user(empty_session, values=None):
    new_user_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_user_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                          {'user_name': new_user_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where user_name = :user_name',
                                {'user_name': new_user_name}).fetchone()
    return row[0]

def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_movie(empty_session):
    empty_session.execute(
        'INSERT INTO movies (title, release_year, description, runtime_minutes, external_rating, external_rating_votes, revenue, metascore) VALUES '
        '("Step Brothers",'
        '"2006",'
        '"Two middle-aged step brothers must learn to live with each other.",'
        '"124",'
        '"8.1",'
        '"70106",'
        '"313.01",'
        '"76")'
    )
    row = empty_session.execute('SELECT id from movies').fetchone()
    return row[0]



def insert_reviewed_movie(empty_session):
    movie_key = insert_movie(empty_session)
    user_key = insert_user(empty_session)

    timestamp_1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp_2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    empty_session.execute(
        'INSERT INTO reviews (user_id, movie_id, review_text, rating, timestamp) VALUES '
        '(:user_id, :movie_id, "Review 1 text", 8, :timestamp_1),'
        '(:user_id, :movie_id, "Review 2 text", 9, :timestamp_2)',
        {'user_id': user_key, 'movie_id': movie_key, 'timestamp_1': timestamp_1, 'timestamp_2': timestamp_2}
    )

    row = empty_session.execute('SELECT id from movies').fetchone()
    return row[0]

def make_movie():
    a_movie = Movie("Step Brothers", 2006) # this is supposed to match the one made in insert_movie
    a_movie.description = "Two middle-aged step brothers must learn to live with each other."
    a_movie.runtime_minutes = 124
    a_movie.external_rating = 8.1
    a_movie.external_rating_votes = 70106
    a_movie.revenue = 313.01
    a_movie.metascore = 76
    return a_movie

def make_user():
    a_user = User("Andrew", "111")
    return a_user

def test_loading_of_users(empty_session):
    users = list()
    users.append(("andrew", "1234")) # covid one doesn't care about lowercase usernames, I have adjusted accordingly
    users.append(("cindy", "1111")) # e.g. User("blah", "blah") will make the username lowercase, hence for what we put in the databsae to match that, we have to make what we put in the database lowercase
    insert_users(empty_session, users)

    expected = [
        User("andrew", "1234"),
        User("cindy", "999")
    ]
    assert empty_session.query(User).all() == expected

def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name, password FROM users'))
    assert rows == [("andrew", "111")]

def test_saving_of_users_with_common_username(empty_session):
    insert_user(empty_session, ("andrew", "1234")) # ditto above re: covid not caring about lower case, so I have adjusted accordingly
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("andrew", "111")
        empty_session.add(user)
        empty_session.commit()

def test_loading_of_movie(empty_session):
    movie_key = insert_movie(empty_session)
    expected_movie = make_movie()
    fetched_movie = empty_session.query(Movie).one()

    assert expected_movie == fetched_movie
    assert movie_key == fetched_movie.id
    

def test_loading_of_reviewed_movie(empty_session):
    insert_reviewed_movie(empty_session)

    rows = empty_session.query(Movie).all()
    a_movie = rows[0]

    assert len(a_movie.review_list) == 2

    for a_review in a_movie.review_list:
        assert a_review.movie is a_movie

def test_saving_of_review(empty_session):
    movie_key = insert_movie(empty_session)
    user_key = insert_user(empty_session, ("andrew", "1234"))

    rows = empty_session.query(Movie).all()
    a_movie = rows[0]
    a_user = empty_session.query(User).filter_by(_User__user_name = "andrew").one()

    # Create a new Comment that is bidirectionally linked with the User and Article.
    review_text = "Some review text."
    a_review = make_review(a_user, a_movie, review_text, 10)

    # Note: if the bidirectional links between the new Comment and the User and
    # Article objects hadn't been established in memory, they would exist following
    # committing the addition of the Comment to the database.
    empty_session.add(a_review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_id, movie_id, review_text FROM reviews'))

    assert rows == [(user_key, movie_key, review_text)]

def test_saving_of_movie(empty_session):
    a_movie = make_movie()
    empty_session.add(a_movie)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT title, release_year, description, runtime_minutes, external_rating, external_rating_votes, revenue, metascore FROM movies'))
    assert rows == [("Step Brothers", 2006, "Two middle-aged step brothers must learn to live with each other.", 124, 8.1, 70106, 313.01, 76)]

def test_save_reviewed_movie(empty_session):
    # Create Article User objects.
    a_movie = make_movie()
    a_user = make_user()

    # Create a new Comment that is bidirectionally linked with the User and Movie.
    review_text = "Some review text."
    a_review = a_review = make_review(a_user, a_movie, review_text, 10)

    # Save the new Movie.
    empty_session.add(a_movie)
    empty_session.commit()

    # Test test_saving_of_movie() checks for insertion into the movies table.
    rows = list(empty_session.execute('SELECT id FROM movies'))
    movie_key = rows[0][0]

    # Test test_saving_of_users() checks for insertion into the users table.
    rows = list(empty_session.execute('SELECT id FROM users'))
    user_key = rows[0][0]

    # Check that the comments table has a new record that links to the movies and users
    # tables.
    rows = list(empty_session.execute('SELECT user_id, movie_id, review_text FROM reviews'))
    assert rows == [(user_key, movie_key, review_text)]