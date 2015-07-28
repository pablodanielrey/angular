class File:

    '''
    table file.file (
        id varchar not null primary key,
        name varchar,
        hash varchar,
        data bytea
    )
    '''

    '''
        Retorna el id del archivo
    '''
    def persist(self,con,file):
        '''
            falta implementar
        '''

    def findById(self,con, id):
        '''
            falta implementar
        '''

    def search(self,con,text):
        '''
            falta implementar
        '''

    def delete(self,con,id):
        '''
            falta implementar
        '''
