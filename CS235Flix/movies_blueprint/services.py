from CS235Flix.domain.review import make_review


def get_all_movies(a_repo_instance):
    movie_list = a_repo_instance.get_all_movies()
    movie_dict_list = movies_to_dict(movie_list)
    #print(movie_list) # for debugging
    return movie_dict_list

def get_movie(title, release_year, a_repo_instance):
    a_movie = a_repo_instance.get_movie(title, release_year)
    a_movie_dict = movie_to_dict(a_movie)
    return a_movie_dict

def add_review(user_name, movie_title, movie_release_year, review_text, rating, a_repo_instance):
    a_user = a_repo_instance.get_user(user_name)
    a_movie = a_repo_instance.get_movie(movie_title, movie_release_year)
    make_review(a_user, a_movie, review_text, rating)

def get_movies_with_actor_director_or_genre(actor_full_name, director_full_name, genre_name, a_repo_instance):
    movie_list = a_repo_instance.get_movies_with_actor_director_or_genre(actor_full_name, director_full_name, genre_name)
    movie_dict_list = movies_to_dict(movie_list)
    return movie_dict_list

##########################################
# Domain Model objects ->  Dictionaries
##########################################
def review_to_dict(a_review):
    date = a_review.timestamp.date()
    time = a_review.timestamp.time()
    simplified_date_and_time = "{} at {}:{}:{}".format(date, time.hour, time.minute, time.second)

    a_review_dict = {
        'review_text': a_review.review_text,
        'rating': a_review.rating,
        'timestamp': simplified_date_and_time,
        'user_name': a_review.user.user_name # hmmm
    }
    return a_review_dict

def reviews_to_dict(review_list):
    review_dict_list = [review_to_dict(a_review) for a_review in review_list]
    return review_dict_list


def movie_to_dict(a_movie):
    a_movie_dict = {
        'title': a_movie.title,
        'release_year': a_movie.release_year,
        'runtime_minutes': a_movie.runtime_minutes,
        'description': a_movie.description,
        'director': director_to_string(a_movie.director),
        'actors': actors_to_string(a_movie.actors),
        'genres': genres_to_string(a_movie.genres),
        'external_rating': a_movie.external_rating,
        'external_rating_votes': a_movie.external_rating_votes,
        'revenue': a_movie.revenue,
        'metascore': a_movie.metascore,
        'review_list': reviews_to_dict(a_movie.review_list)
    }
    return a_movie_dict

def movies_to_dict(movie_list):
    movie_dict_list = [movie_to_dict(a_movie) for a_movie in movie_list]
    return movie_dict_list

def director_to_string(a_director):
    return a_director.director_full_name

def actor_to_string(a_actor):
    return a_actor.actor_full_name

def actors_to_string(actor_list):
    actor_string_list = [actor_to_string(a_actor) for a_actor in actor_list]
    return ", ".join(actor_string_list)

def genre_to_string(a_genre):
    return a_genre.genre_name

def genres_to_string(genre_list):
    genre_string_list = [genre_to_string(a_genre) for a_genre in genre_list]
    return ", ".join(genre_string_list)

"""
def director_to_dict(a_director):
    a_director_dict = {
        'director_full_name': a_director.director_full_name
    }
    return a_director_dict

def directors_to_dict(director_list):
    director_dict_list = [director_to_dict(a_director) for a_director in director_list]
    return director_dict_list

def actor_to_dict(a_actor):
    a_actor_dict = {
        'actor_full_name': a_actor.actor_full_name,
        'colleague_list': a_actor.colleague_list
    }
    return a_actor_dict

def actors_to_dict(actor_list):
    actor_dict_list = [actor_to_dict(a_actor) for a_actor in actor_list]
    return actor_dict_list

def genre_to_dict(a_genre):
    a_genre_dict = {
        'genre_name': a_genre.genre_name
    }
    return a_genre_dict

def genres_to_dict(genre_list):
    genre_dict_list = [genre_to_dict(a_genre) for a_genre in genre_list]
    return genre_dict_list
"""