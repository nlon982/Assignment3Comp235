import pytest

from flask import session


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid username and password.
    response = client.post(
        '/authentication/register',
        data={'username': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Your username is required'),
        ('cj', '', b'Your username is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
        ('fmercury', 'Test#6^0', b'Your username is already taken - please supply another'),
))
def test_register_with_invalid_input(client, username, password, message):
    # Check that attempting to register with invalid combinations of username and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['username'] == 'thorke'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session

def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'Lorem ipsum dolor sit amet' in response.data

def test_login_required_to_review(client):
    response = client.post('/review', data={'movie_title': "Guardians of the Galaxy", 'movie_release_year': 2014})
    assert response.headers['Location'] == 'http://localhost/authentication/login'

def test_review(client, auth):
    # Login a user.
    auth.login()

    # Check that we can retrieve the review page.
    response = client.get('review?movie_title=Guardians+of+the+Galaxy&movie_release_year=2014')

    response = client.post('/review', data={'movie_title': "Guardians of the Galaxy", 'movie_release_year': 2014, 'review': 'Haha, this movie was so good, I love it.', 'rating': '7.6'})
    assert response.headers['Location'] == 'http://localhost/browse'

    # Test that review is there (awesome guardians of the galaxy is on the first page, which it is with this data)
    response = client.get('/browse')
    assert b'Haha, this movie was so good, I love it.' in response.data
    assert b'7.6' in response.data


@pytest.mark.parametrize(('review_text', 'rating', 'messages'), (
        ('Who thinks the director is a fuckwit?', '8', (b'Your comment must not contain profanity')),
        ('Hey', '8', (b'Your review is too short')),
        ('This is so good, I just loved this movie', '81', (b'Please choose a number between 0 and 10')),
        ('ass', '64', (b'Your review is too short', b'Your review must not contain profanity', b'Please choose a number between 0 and 10')),
))
def test_review_with_invalid_input(client, auth, review_text, rating, messages):
    # Login a user.
    auth.login()

    # Attempt to comment on an article.
    response = client.post('/review', data={'movie_title': "Guardians of the Galaxy", 'movie_release_year': 2014, 'review': review_text, 'rating': rating})
    # Check that supplying invalid comment text generates appropriate error messages.
    for message in messages:
        assert message in response.data

def test_browse_movies(client): # see if reviews are there
    response = client.get('/browse')
    assert response.status_code == 200

    assert b'Guardians of the Galaxy' in response.data # note response.data is the html

def test_search_movies(client):
    response = client.get('/browse?actor_to_filter={}&director_to_filter={}&genre_to_filter={}'.format("Chris Pratt", "", ""))
    assert response.status_code == 200
    assert b'Chris Pratt' in response.data # I could check all movies on the page have Chris Pratt but that'd require a lot of logic to program, or it'd require knowing the amount of movies on the page (which is decided in the request handler)

    response = client.get('/browse?actor_to_filter={}&director_to_filter={}&genre_to_filter={}'.format("", "M. Night Shyamalan", ""))
    assert response.status_code == 200
    assert b'M. Night Shyamalan' in response.data # ^ ditto

    response = client.get('/browse?actor_to_filter={}&director_to_filter={}&genre_to_filter={}'.format("", "", "Adventure"))
    assert response.status_code == 200
    assert b'Adventure' in response.data # ^ ditto

    # assuming they work in unison i.e. if you enter "Chris Pratt" "M.Night Shyamalan" and "Adventure" you get ALL movies with those
    # ^ there not a good way to check at this "level of abstraction" i.e. the html without going through all cursors (whereas I good time to test this is in the service layer)




