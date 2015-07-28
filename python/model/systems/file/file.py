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


    def findById(self,con, id):


    def search(self,con,text):

    def delete(self,con,id):
