def get_genre_hash(genre_name):
    return hash(genre_name)

class Genre:
    def __init__(self, genre_name):
        if genre_name == "" or type(genre_name) != str:
            self.__genre_name = None
        else:
            self.__genre_name = genre_name

    @property
    def genre_name(self):
        return self.__genre_name

    def __repr__(self):
        return "<Genre {}>".format(self.__genre_name)

    def __eq__(self, other):
        return isinstance(other, Genre) and self.__genre_name == other.genre_name # other's genre_name is private, using the @property method

    def __lt__(self, other):
        return self.__genre_name < other.genre_name

    def __hash__(self): # "defines which attribute is used for computing a hash", more like "returns a hash, which you can just ask it to hash an attribute"
        return get_genre_hash(self.__genre_name)

"""
Assuming by "The class should allow access to the
ame of the genre through the genre_name property."
Property, as in, they're not calling an attribute a property,
I.e. I should make a private attribute, and give access to it
via @property
"""