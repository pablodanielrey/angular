# -*- coding: utf-8 -*-
import logging, inject, time, sys, signal
import psycopg2, uuid
import datetime

sys.path.append('../python')

from model.config import Config
from model.utils import Periodic
from model.users.users import Users
from model.systems.assistance.logs import Logs
from model.systems.assistance.date import Date
from model.systems.assistance.offices.offices import Offices

from zksoftware.zkSoftware import ZkSoftware



class Main:

    config = inject.attr(Config)
    logs = inject.attr(Logs)
    users = inject.attr(Users)
    date = inject.attr(Date)
    offices = inject.attr(Offices)

    def __init__(self):
        host = self.config.configs['zksoftware_host']
        port = int(self.config.configs['zksoftware_port'])
        self.zk = ZkSoftware(host,port)

        self.timezone = self.config.configs['zksoftware_timezone']


    def _connect(self):
        host = self.config.configs['database_host']
        db = self.config.configs['database_database']
        user = self.config.configs['database_user']
        passw = self.config.configs['database_password']
        con = psycopg2.connect(host=host, dbname=db, user=user, password=passw)
        return con


    def sincLogs(self):
        try:
            logging.debug('Conectandose al reloj y obteniendo logs')

            logs = self.zk.getAttLog()
            if len(logs) <= 0:
                logging.debug('No se encontraron los a sincronizar')
                return

            logging.info('{} logs obtenidos del reloj'.format(len(logs)))

            con = self._connect()
            try:
                logging.info('transformando logs al formato del sistema')
                tlogs = []
                for l in logs:
                    logging.debug(l)

                    dni = l['PIN']
                    user = self.users.findUserByDni(con,dni)
                    userId = None
                    if user is None:
                        newUser = {
                                'dni':l['PIN'],
                                'name':'autogenerado asistencia',
                                'lastname':'autogenerado asistencia'
                        }
                        userId = self.users.createUser(con,newUser)

                        ''' agrego la persona a la oficina de asistencia autogenerados - el id esta en insert_basic_data.sql '''
                        self.offices.addUserToOffices(con,'45cc065a-7033-4f00-9b19-d7d097129db3',userId)
                    else:
                        userId = user['id']

                    date = l['DateTime']
                    aware = self.date.localize(self.timezone,date)
                    utcaware = self.date.awareToUtc(aware)

                    l2 = {
                        'id':str(uuid.uuid4()),
                        'userId':userId,
                        'deviceId':self.config.configs['zksoftware_device_id'],
                        'verifymode':l['Verified'],
                        'log':utcaware
                    }
                    tlogs.append(l2)

                logging.info('salvando logs en la base')
                for l in tlogs:
                    logging.debug(l)
                    if self.logs.findLogByDate(con,l['log']) is None:
                        self.logs.persist(con,l)
                    else:
                        logging.warn('{} ya existente'.format(l))

                con.commit()


                """ borro los logs del reloj """
                nowdate = datetime.datetime.now()
                deletestart = nowdate.replace(hour=int(self.config.configs['zksoftware_hour_start_delete']),minute=int(self.config.configs['zksoftware_minute_start_delete']),second=0,microsecond=0)
                deleteend = nowdate.replace(hour=int(self.config.configs['zksoftware_hour_end_delete']),minute=int(self.config.configs['zksoftware_minute_end_delete']),second=0,microsecond=0)
                if (nowdate <= deleteend and nowdate >= deletestart):
                    logscheck = self.zk.getAttLog()
                    logslen = len(logs)
                    logschecklen = len(logscheck)
                    if logslen == logschecklen:

                        logs.sort(key=lambda x: x['DateTime'])
                        logscheck.sort(key=lambda x: x['DateTime'])
                        equals = True
                        for i in range(len(logs)):
                            if logs[i]['DateTime'] != logscheck[i]['DateTime'] or logs[i]['PIN'] != logscheck[i]['PIN']:
                                equals = False
                                break

                        if equals:
                            logging.info('Eliminando {} logs del reloj'.format(logslen))
                            self.zk.clearAttLogs()

            finally:
                con.close()

        except Exception as e:
            logging.exception(e)




def _sincLogs(main):
    main.sincLogs()


def config_injector(binder):
    binder.bind(Config,Config('firmware-config.cfg'))


if __name__ == '__main__':

    """
    if len(sys.argv) <= 1:
        print('Debe pasar como parámetro la ip del reloj y el puerto.')
        print('Ej:')
        print('python ' + sys.argv[0] + ' 127.0.0.1 8080')
        sys.exit(1)
    """

    logging.basicConfig(filename='/var/log/firmware-sync.log',format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

    inject.configure(config_injector)
    config = inject.instance(Config)

    logging.info('Iniciando el sincronizador de logs')

    main = Main()
    rt = Periodic(10 * 60, _sincLogs,main)

    def close_sig_handler(signal,frame):
        logging.info('Cerrando sistema sincronizador')
        rt.stop()
        sys.exit()

    signal.signal(signal.SIGINT,close_sig_handler)

    while True:
        time.sleep(1000)
