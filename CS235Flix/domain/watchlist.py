from CS235Flix.domain.movie import Movie

class WatchList:
    def __init__(self):
        self.__watch_list = list()

    def add_movie(self, a_movie):
        if type(a_movie) == Movie: # the requirements were vague on if they wanted type safety, doing it just in case
            if a_movie not in self.__watch_list:
                self.__watch_list.append(a_movie)

    def remove_movie(self, a_movie):
        if a_movie in self.__watch_list:
            self.__watch_list.remove(a_movie)


    def size(self):
        return len(self.__watch_list)

    def select_movie_to_watch(self, a_index):
        # I remember reading online that in fact it's considered
        # "clean" to use exceptions instead of doing it the slow way
        # i.e. instead of checking if a list is big enough to have a certain index,
        # just try it, and see if it gives an error
        # this also has the benefit that if a weird index is given (e.g. a string)
        # it's no problem
        try:
            return self.__watch_list[a_index]
        except:
            return None

    def first_movie_in_watchlist(self):
        return self.select_movie_to_watch(0)
        # this uses dependency inversion principle (I think?) in the
        # sense that instead of getting this to depend on some low-level
        # logic, like in the method above - i'll reuse the above method (which we
        # can call 'higher level' logic, since it uses low-level logic)
        # the benefit being if the implementation of the watch list
        # changes, I ONLY have to update the above method

        # the downside is if the requirements shift later on to return
        # something other than None.

    def __iter__(self):
        return iter(self.__watch_list)
        # no need to reinvent the wheel, this returns the iterable object
        # of list (which has __next__ defined)

