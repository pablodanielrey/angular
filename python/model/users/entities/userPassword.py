from model.entity import Entity

class UserPassword(Entity):

    def __init__(self):
        self.id = None
        self.userId = None
        self.username = None
        self.password = None
