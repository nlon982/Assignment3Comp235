from datetime import datetime


class Review:
    def __init__(self, a_user, a_movie, review_text, rating):
        self.__movie = a_movie # assuming movie object
        self.__user = a_user

        if type(review_text) == str: # assuming they want that
            self.__review_text = review_text
        else:
            self.__review_text = ""


        if rating >= 1 and rating <= 10:
            self.__rating = rating
        else:
            self.__rating = None

        self.__timestamp = datetime.today() # a datetime object contains the data and the time

    @property
    def user(self):
        return self.__user

    @property
    def movie(self):
        return self.__movie

    @property
    def review_text(self):
        return self.__review_text

    @property
    def rating(self):
        return self.__rating

    @property
    def timestamp(self):
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, a_timestamp): # probably not "secure" to have a setter for this, but it's convenient for the below, so I don't have to include timestamp in the init
        self.__timestamp = a_timestamp

    def __repr__(self):
        timestamp = self.__timestamp
        return "<Review {} {}, {}, {} ({}-{}-{})>".format(self.__movie.title, self.__movie.release_year, self.__review_text, self.__rating, timestamp.day, timestamp.month, timestamp.year)

    def __eq__(self, other):
        return (self.__movie == other.movie) and (self.__review_text == other.review_text) and (self.__rating == other.rating) and (self.__timestamp == other.timestamp)

def make_review(a_user, a_movie, review_text, rating, timestamp = None): # set up two directional association (is that the wording?)
    # assumes everything is of correct type
    a_review = Review(a_user, a_movie, review_text, rating)
    # if timestamp is None, do nothing (i.e. let timestamp be the current date/time)
    if timestamp != None:
        a_review.timestamp = timestamp
    a_user.add_review(a_review)
    a_movie.add_review(a_review)
    return a_review

