from model.entity import Entity
from model.users.entities.user import User

class Inscription(Entity):

    def __init__(self):
        self.id = None
        self.userId = None
        self.degree = None
        self.workType = None
        self.reside = False
        self.travel = False
        self.workExperience = False
        self.checked = False
        self.created = None
        self.average1 = 0
        self.average2 = 0
        self.approved = 0

    def getUser(self, ctx):
        return ctx.dao(ctx).findByIds(con, [self.userId])
