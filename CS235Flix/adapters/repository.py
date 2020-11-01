import abc

repo_instance = None

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_movie(self, a_movie):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, title, release_year):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_movies(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_director(self, a_director):
        raise NotImplementedError

    @abc.abstractmethod
    def get_director(self, director_full_name):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_directors(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_actor(self, a_actor):
        raise NotImplementedError

    @abc.abstractmethod
    def get_actor(self, actor_full_name):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_actors(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, a_genre):
        raise NotImplementedError

    @abc.abstractmethod
    def get_genre(self, genre_name):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_genres(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_users(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_with_actor(self, actor_full_name):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_with_director(self, director_full_name):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_with_genre(self, genre_name):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_with_actor_director_or_genre(self, actor_full_name, director_full_name, genre_name): # the key word is "or", as in, it takes the union of movies it finds with this actor, director and genre
        raise NotImplementedError

    #@abc.abstractmethod
    #def add_review(self, a_review): # really not much point in these
    #    raise NotImplementedError

    #@abc.abstractmethod
    #def get_reviews(self): # ^ ditto
    #    raise NotImplementedError
