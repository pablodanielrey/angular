
from actions.systems.assistance.export import ExportModelBase
from model.assistance.utils import Utils
import datetime
import pyoo
import uuid

class ExportModel(ExportModelBase):

    @classmethod
    def exportStatistics(cls, ownerId, stats, usersData):
        classfiedUsersData = cls.classifyUserData(usersData)

        justifications = {}

        try:
            calc = pyoo.Desktop('163.10.56.57', 2002)
            doc = calc.create_spreadsheet()
            try:
                sheet = doc.sheets[0]
                i = 0
                for stat in stats:
                    user = classfiedUsersData[stat.userId]
                    sheet[i,1].value = user.name
                    sheet[i,2].value = user.lastname
                    sheet[i,3].value = user.dni
                    sheet[i,4].value = stat.position
                    sheet[i,5].value = Utils._naiveFromLocalAware(Utils.toLocalFromAware(stat.scheduleStart)) if stat.scheduleStart is not None else ''
                    sheet[i,6].value = Utils._naiveFromLocalAware(Utils.toLocalFromAware(stat.scheduleEnd)) if stat.scheduleEnd is not None else ''
                    sheet[i,7].value = Utils._naiveFromLocalAware(Utils.toLocalFromAware(stat.logStart)) if stat.logStart is not None else ''
                    sheet[i,8].value = Utils._naiveFromLocalAware(Utils.toLocalFromAware(stat.logEnd)) if stat.logEnd is not None else ''
                    sheet[i,9].value = datetime.timedelta(seconds=stat.workedSeconds)
                    i = i + 1

                fn = '{}/{}.xlsx'.format('/tmp',str(uuid.uuid4()))
                logging.info('salvando : {}'.format(fn))
                doc.save(fn, pyoo.FILTER_EXCEL_2007)
                return fn

            finally:
                doc.close()

        except Exception as e:
            logging.error('No se puede conectar al servidor de exportación')
            raise e


    @classmethod
    def exportLogs(cls, ownerId, logs, usersData):
        classfiedUsersData = cls.classifyUserData(usersData)

        try:
            calc = pyoo.Desktop('163.10.56.57', 2002)
            doc = calc.create_spreadsheet()
            try:
                sheet = doc.sheets[0]
                i = 0
                for log in logs:
                    user = classfiedUsersData[log.userId]
                    sheet[i,1].value = user.name
                    sheet[i,2].value = user.lastname
                    sheet[i,3].value = user.dni
                    sheet[i,4].value = log.verifyMode
                    sheet[i,5].value = Utils._naiveFromLocalAware(log.log) if log.log is not None else ''
                    sheet[i,6].value = Utils._naiveFromLocalAware(log.log) if log.log is not None else ''
                    i = i + 1

                fn = '{}/{}.xlsx'.format('/tmp',str(uuid.uuid4()))
                logging.info('salvando : {}'.format(fn))
                doc.save(fn, pyoo.FILTER_EXCEL_2007)
                return fn

            finally:
                doc.close()

        except Exception as e:
            logging.error('No se puede conectar al servidor de exportación')
            raise e
