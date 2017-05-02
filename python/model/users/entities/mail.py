from model import Ids
from model.entity import Entity

class Mail(Entity):

    def __init__(self):
        self.id = None
        self.userId = None
        self.email = None
        self.confirmed = False
        self.hash = None
        self.created = None

    def confirm(self, ctx):
        ''' cambia el estado a confirmado '''
        if self.confirmed:
            return
        self.confirmed = True
        return self.persist(ctx)
