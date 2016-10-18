

class ExportModelBase:
    '''
        Clase base para las exportaciones.
    '''

    @classmethod
    def classifyUserData(cls, usersData):
        classifiedUsersData = {}
        for user in usersData:
            classifiedUsersData[user.id] = user
        return classifiedUsersData

    @classmethod
    def exportLogs(cls, logs, usersData):
        raise Exception('not implemented')

    @classmethod
    def exportStatistics(cls, stats, usersData):
        raise Exception('not implemented')
