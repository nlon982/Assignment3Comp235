from CS235Flix.domain.person import Person

class Actor(Person): # I haven't warmed up to superclasses in Python yet, this feels weird
    def __init__(self, actor_full_name):
        super().__init__(actor_full_name)
        self.__colleague_list = list()

    @property
    def actor_full_name(self):
        return self.full_name

    def __repr__(self):
        return "<Actor {}>".format(self.full_name)

    def add_actor_colleague(self, colleague):
        if self.check_if_this_actor_worked_with(colleague) == False: # may as well use it?...
            self.__colleague_list.append(colleague)

    def check_if_this_actor_worked_with(self, colleague):
        return colleague in self.__colleague_list
