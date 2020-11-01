from CS235Flix.domain.person import Person

class Director(Person):

    def __init__(self, director_full_name: str):
        super().__init__(director_full_name)

    @property
    def director_full_name(self) -> str: # feels a bit gross that this can't be inherited
        return self.full_name # __full_name is private in Person, so can't be accessed here

    def __repr__(self):
        return "<Director {}>".format(self.full_name)

"""
class TestDirectorMethods:

    def test_init(self):
        director1 = Director("Taika Waititi")
        assert repr(director1) == "<Director Taika Waititi>"
        director2 = Director("")
        assert director2.director_full_name is None
        director3 = Director(42)
        assert director3.director_full_name is None
        director4 = Director("Ben Zebra")
        assert director4 < director1 == True
"""