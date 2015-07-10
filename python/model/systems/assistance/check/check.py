'''
    Clase base de todos los tipos de chequeo
'''
class Check:

    '''
        verifica si el tipo de chequeo es el que corresponde con el date
    '''
    @classmethod
    def isActualCheck(cls,date,check):
        if (date >= check['start']):
            if check['end'] is None:
                return True
            elif date < c['end']:
                return True
        return False



    '''
        verifica si es mismo tipo de chequeo
    '''
    def isTypeCheck(self,type):
        raise Exception('abstract')


    '''
        Obtiene las fallas
        return
        fail: {
            'userId':'',
            'date':date,
            'description':'Sin marcación',
            'justifications':[]
        }
        actualDate es aware.
    '''
    def getFails(self, utils, userId, actualDate, justifications, con):
        raise Exception('abstract')
