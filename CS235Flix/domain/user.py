def get_user_hash(user_name):
    return hash(user_name)

class User:
    def __init__(self, user_name, password):
        # assuming user_name and password are strings
        self.__user_name = user_name.strip().lower()
        self.__password = password

        self.__watched_movies = list()
        self.__reviews = list()
        self.__time_spent_watching_movies_minutes = 0 # necessary to start at 0

    @property
    def user_name(self):
        return self.__user_name

    @property
    def password(self):
        return self.__password

    @property
    def watched_movies(self):
        return self.__watched_movies

    @property
    def reviews(self):
        return self.__reviews

    @property
    def time_spent_watching_movies_minutes(self):
        return self.__time_spent_watching_movies_minutes

    def __repr__(self):
        return "<User {}>".format(self.__user_name)

    def __eq__(self, other):
        return self.__user_name == other.user_name

    def __lt__(self, other):
        return self.__user_name < other.user_name

    def __hash__(self):
        return get_user_hash(self.__user_name) # since a unique reprsentation is deemed by user name (quote coderunner), i'll use this as a hash

    def watch_movie(self, a_movie):
        # assuming passed a movie object WITH a runtime
        self.__watched_movies.append(a_movie)
        self.__time_spent_watching_movies_minutes += a_movie.runtime_minutes

    def add_review(self, a_review):
        # assuming passed a review object
        self.__reviews.append(a_review)

