from CS235Flix.domain.actor import Actor
from CS235Flix.domain.genre import Genre
from CS235Flix.domain.director import Director
from CS235Flix.domain.review import Review


def get_movie_hash(title, release_year):
    return hash(title + str(release_year))

class Movie:
    def __init__(self, title, release_year):
        if title == "" or type(title) != str:
            self.__title = None
        else:
            self.__title = title.strip()  # would be less repeated codes to user setter method?

        if type(release_year) == int and release_year >= 1900: # using short circuiting to avoid an error being thrown if incorrect type
            self.__release_year = release_year
        else:
            self.__release_year = None
        # ^ would be less repeated code to use setter methods for those

        self.__description = None
        self.__director = None
        self.__actors = list()
        self.__genres = list()
        self.__runtime_minutes = None

        # more (not required)
        self.__external_rating = None
        self.__external_rating_votes = None # was referred to as "rating votes" but "external rating votes" is more descriptive
        self.__revenue = None
        self.__metascore = None

        self.__review_list = list()

    #------------------------ getter and setter methods (for all attributes except year)
    @property
    def review_list(self):
        return self.__review_list

    @review_list.setter
    def review_list(self, review_list):
        for a_review in review_list:
            if type(a_review) == Review and a_review.movie == self: # uses short-circuiting
                self.__review_list.append(a_review)

    def add_review(self, a_review):
        if type(a_review) == Review and a_review.movie == self:  # ^ ditto
            self.__review_list.append(a_review)

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, a_title):
        if a_title != "" and type(a_title) == str:
            self.__title = a_title.strip()
        else:
            self.__title = None

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, a_description):
        if type(a_description) == str:
            self.__description = a_description.strip()
        else:
            self.__description == None

    @property
    def director(self):
        return self.__director

    @director.setter
    def director(self, a_director):
        if type(a_director) == Director:
            self.__director = a_director

    @property
    def actors(self):
        return self.__actors

    @actors.setter
    def actors(self, actor_list):
        self.__actor_list = list()
        for a_actor in actor_list:
            if type(a_actor) == Actor:
                self.__actors.append(a_actor)

    @property
    def genres(self):
        return self.__genres

    @genres.setter
    def genres(self, genre_list):
        self.__genre_list = list()
        for a_genre in genre_list:
            if type(a_genre) == Genre:
                self.__genres.append(a_genre)

    @property
    def runtime_minutes(self):
        return self.__runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, runtime_minutes):
        # i'll assume a number is passed
        if runtime_minutes > 0:
            self.__runtime_minutes = round(runtime_minutes)
        else:
            raise ValueError # as requested

        # more getter and setters (not required)

    # ------------------------ More getter and setter methods

    @property
    def external_rating(self):
        return self.__external_rating

    @external_rating.setter
    def external_rating(self, an_external_rating):
        # assuming a number passed
        if an_external_rating >= 0 and an_external_rating <= 10:  # what I can gather from CSV
            self.__external_rating = an_external_rating
        else:
            raise ValueError  # assuming they'll want this

    @property
    def external_rating_votes(self):
        return self.__external_rating_votes

    @external_rating_votes.setter
    def external_rating_votes(self, an_external_rating_votes):
        # assuming a number passed
        if an_external_rating_votes >= 0:  # obvious requirement
            self.__external_rating_votes = an_external_rating_votes
        else:
            raise ValueError  # assuming they'll want this

    @property
    def revenue(self):
        return self.__revenue

    @revenue.setter
    def revenue(self, a_revenue):
        if a_revenue >= 0:  # a requirement, I think? Can revenue be negative?
            self.__revenue = a_revenue
        else:
            raise ValueError  # assuming they'll want this

    @property
    def metascore(self):
        return self.__metascore

    @metascore.setter
    def metascore(self, a_metascore):
        if a_metascore >= 0:  # I think this is a requirement?
            self.__metascore = a_metascore
        else:
            raise ValueError  # assuming they'll wannt this

    # they missed out having a getter and setter for year, putting it in for the sake of cleanliness
    @property
    def release_year(self):
        return self.__release_year

    @release_year.setter
    def release_year(self, a_release_year):
        # assumming year is a number
        if type(a_release_year) == int and a_release_year >= 1900:
            self.__release_year = a_release_year

    #------------------------  other methods
    def add_actor(self, a_actor):
        if type(a_actor) == Actor: # assuming they want this
            if a_actor not in self.__actors:
                self.__actors.append(a_actor)
        # unsure if they want to throw an error

    def remove_actor(self, a_actor):
        if type(a_actor) == Actor:  # so it doesn't throw an error when using 'in' below
            if a_actor in self.__actors: # necessary because remove raises a ValueError if not found
                self.__actors.remove(a_actor)
        # they asked to NOT throw an error (hence above)

    def add_genre(self, a_genre):
        if type(a_genre) == Genre:
            if a_genre not in self.__genres:
                self.__genres.append(a_genre)

    def remove_genre(self, a_genre):
        if type(a_genre) == Genre:
            if a_genre in self.__genres:
                self.__genres.remove(a_genre)

    #------------------------  special methods, aka magic methods
    def __repr__(self):
        return "<Movie {}, {}>".format(self.__title, self.__release_year)

    def __eq__(self, other): # Assumes title IS case sensitive
        if type(other) == Movie:
            return (self.__title == other.title) and (self.__release_year == other.release_year)
        else:
            return False

    def __lt__(self, other): # sorting by title then release year
        if self.__title == other.title:
            return self.__release_year < other.release_year
        else:
            return self.__title < other.title

    def __hash__(self):
        return get_movie_hash(self.__title, self.__release_year)