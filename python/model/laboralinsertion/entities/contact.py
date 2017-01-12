from model.entity import Entity

class Contact(Entity):

    ''' datos de los contactos de la empresa '''
    def __init__(self):
        self.name = ''
        self.email = ''
        self.telephone = ''
        self.companyId = ''
        self.id = ''
