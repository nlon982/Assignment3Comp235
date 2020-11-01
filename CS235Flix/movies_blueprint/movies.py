from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, FloatField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange


import CS235Flix.movies_blueprint.services as services

import CS235Flix.adapters.repository as repo
from CS235Flix.authentication_blueprint.authentication import login_required
from CS235Flix.domain.movie import Movie, get_movie_hash

# Configure Blueprint.
movies_blueprint = Blueprint('movies_bp', __name__)


@movies_blueprint.route('/browse', methods=['GET'])
def browse():
    movies_per_page = 5

    cursor = request.args.get('cursor')
    actor_to_filter = request.args.get('actor_to_filter') # this is in the form of the actor's full name
    director_to_filter = request.args.get('director_to_filter')  # this is in the form of the director's full name
    genre_to_filter = request.args.get('genre_to_filter')  # this is in the form of the genre's name
    # note the above are None if they don't exist

    if cursor is None:
        # no cursor parameter, so start at the beginning
        cursor = 0
    else:
        cursor = int(cursor)

    repo_instance = repo.repo_instance
    if actor_to_filter == None and director_to_filter == None and genre_to_filter == None:
        movies = services.get_all_movies(repo_instance) # running the below would work too (i.e. with Nones), this call is just way more efficient
    else:
        movies = services.get_movies_with_actor_director_or_genre(actor_to_filter, director_to_filter, genre_to_filter, repo_instance)

    #print("##################################")
    #print(services.get_all_movies(repo_instance)[0]["review_list"])
    #print("##################################")

    movies_to_show = movies[cursor: cursor + movies_per_page]

    prev_page_url = None
    first_page_url = None
    next_page_url = None
    last_page_url = None

    if cursor > 0:  # inherently means not on the first page
        # ^  this improves what was there initially?
        prev_page_url = url_for('movies_bp.browse', cursor = cursor - movies_per_page, actor_to_filter = actor_to_filter, director_to_filter = director_to_filter, genre_to_filter = genre_to_filter)
        first_page_url = url_for('movies_bp.browse', actor_to_filter = actor_to_filter, director_to_filter = director_to_filter, genre_to_filter = genre_to_filter)  # as above, this has the effect of having cursor = 0

    if cursor + movies_per_page < len(movies):  # there are further articles than what's on the current page
        # ^ this logic works if your cursor starts at 0
        next_page_url = url_for('movies_bp.browse', cursor = cursor + movies_per_page, actor_to_filter = actor_to_filter, director_to_filter = director_to_filter, genre_to_filter = genre_to_filter)

        amount_of_pages_floor = len(movies) // movies_per_page
        last_cursor = movies_per_page * amount_of_pages_floor

        if len(movies) % movies_per_page == 0:  # last page will have nothing on it
            last_cursor -= movies_per_page  # the last page will have movies_per_page amount of things on it

        last_page_url = url_for('movies_bp.browse', cursor = last_cursor, actor_to_filter = actor_to_filter, director_to_filter = director_to_filter, genre_to_filter = genre_to_filter)


    for a_movie_dict in movies_to_show:
        a_movie_dict['add_review_url'] = url_for('movies_bp.review_movie', movie_title = a_movie_dict["title"], movie_release_year = a_movie_dict["release_year"])

    return render_template('movies/movies.html', movie_dict_list = movies_to_show, prev_page_url = prev_page_url, first_page_url = first_page_url, next_page_url = next_page_url, last_page_url = last_page_url)



@movies_blueprint.route('/movie_page', methods=['GET'])
def movie_page():
    movie_title = request.args.get('movie_title')
    return "This is the page for: {}".format(movie_title)



@movies_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def review_movie():
    # Obtain the username of the currently logged in user.
    username = session['username']

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an article id, when subsequently called with a HTTP POST request, the article id remains in the
    # form.
    form = ReviewForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the comment text has passed data validation.
        # Extract the article id, representing the commented article, from the form.
        movie_title = form.movie_title.data
        movie_release_year = form.movie_release_year.data

        # Use the service layer to store the new review.
        services.add_review(username, movie_title, movie_release_year, form.review.data, form.rating.data, repo.repo_instance)
        #print("**********************************************************************************")
        #print(services.get_all_movies(repo.repo_instance)[0]["review_list"])
        #print("**********************************************************************************")

        # Retrieve the article in dict form.
        a_movie_dict = services.get_movie(movie_title, movie_release_year, repo.repo_instance)

        # Cause the web browser to display the page of all articles that have the same date as the commented article,
        # and display all comments, including the new comment.
        return redirect(url_for('movies_bp.browse'))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the article id, representing the article to comment, from a query parameter of the GET request.
        movie_title = request.args.get('movie_title')
        movie_release_year = int(request.args.get('movie_release_year'))

        # Store the article id in the form.
        form.movie_title.data = movie_title
        form.movie_release_year.data = movie_release_year
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the article id of the article being commented from the form.
        movie_title = form.movie_title.data
        movie_release_year = form.movie_release_year.data

    # For a GET or an unsuccessful POST, retrieve the article to comment in dict form, and return a Web page that allows
    # the user to enter a comment. The generated Web page includes a form object.
    a_movie_dict = services.get_movie(movie_title, movie_release_year, repo.repo_instance)
    return render_template(
        'movies/review_movie.html',
        title='Review Movie',
        a_movie_dict = a_movie_dict,
        form=form,
        handler_url=url_for('movies_bp.review_movie')
    )

@movies_blueprint.route('/search_actor_director_genre', methods=['GET', 'POST'])
def search_actor_director_genre():
    form = SearchActorDirectorGenreForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the comment text has passed data validation.
        # Extract the article id, representing the commented article, from the form.
        actor_full_name = form.actor_full_name.data
        director_full_name = form.director_full_name.data
        genre_name = form.genre_name.data

        # Cause the web browser to display the page of all articles that have the same date as the commented article,
        # and display all comments, including the new comment.
        return redirect(url_for('movies_bp.browse', actor_to_filter = actor_full_name, director_to_filter = director_full_name, genre_to_filter = genre_name))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the article id, representing the article to comment, from a query parameter of the GET request.
        pass
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the article id of the article being commented from the form.
        pass

    # For a GET or an unsuccessful POST, retrieve the article to comment in dict form, and return a Web page that allows
    # the user to enter a comment. The generated Web page includes a form object.
    return render_template(
        'movies/search_actor_director_genre.html',
        title='Search Actor Director Genre',
        form=form,
        handler_url=url_for('movies_bp.search_actor_director_genre')
    )

class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])
    rating = FloatField('Rating (1 to 10)', [
        DataRequired(),
        NumberRange(min = 0, max = 10, message = "Please choose a number between 0 and 10")])
    movie_title = HiddenField("Movie title")
    movie_release_year = HiddenField("Movie release year")
    submit = SubmitField('Submit')

class SearchActorDirectorGenreForm(FlaskForm):
    actor_full_name = TextAreaField('Actor Full Name')
    director_full_name = TextAreaField('Director Full Name')
    genre_name = TextAreaField('Genre Name')
    submit = SubmitField('Submit')