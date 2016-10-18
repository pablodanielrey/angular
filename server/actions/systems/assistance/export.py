

class ExportModelBase:
    '''
        Clase base para las exportaciones.
    '''

    @classmethod
    def exportLogs(cls, logs, usersData):
        raise Exception('not implemented')

    @classmethod
    def exportStatistics(cls, stats, usersData):
        raise Exception('not implemented')
