import abc

def get_person_hash(full_name):
    return hash(full_name)

class Person(abc.ABC):
    def __init__(self, full_name):
        if full_name == "" or type(full_name) != str:
            self.__full_name = None
        else:
            self.__full_name = full_name.strip() # remove spaces before and after

    @property
    def full_name(self):
        return self.__full_name

    @abc.abstractmethod
    def __repr__(self):
        pass

    def __eq__(self, other):
        return isinstance(other, Person) and self.__full_name == other.full_name # makes use of short circuiting

    def __lt__(self, other):
        return self.__full_name < other.full_name

    def __hash__(self):
        return get_person_hash(self.__full_name)