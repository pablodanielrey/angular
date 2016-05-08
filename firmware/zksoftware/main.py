# -*- coding: utf-8 -*-
import logging, inject, time, sys, signal
import uuid
import psycopg2
from psycopg2.extras import DictCursor
import datetime

sys.path.append('../../python')

from model.utils import Periodic
from model.users.users import User
from model.assistance.logs import Log
from model.assistance.utils import Utils
from model.offices.offices import Office
from model.registry import Registry
from zksoftware.zkSoftware import ZkSoftware



class Main:


    #date = inject.attr(Date)

    def __init__(self):
        reg = inject.instance(Registry)

        #parametros generales de zksoftware
        registry = reg.getRegistry('zksoftware')

        self.period = int(registry.get('period'))
        host = registry.get('host')
        port = int(registry.get('port'))
        self.zk = ZkSoftware(host, port)
        self.timezone = registry.get('timezone')
        self.deviceId = registry.get('device_id')

        # parametros que manejan cuando se borran los logs del reloj
        self.hour_start_delete = registry.get('hour_start_delete')
        self.minute_start_delete = registry.get('minute_start_delete')
        self.hour_end_delete = registry.get('hour_end_delete')
        self.minute_end_delete = registry.get('minute_end_delete')

        # parametros de la conexion a la base
        registry = reg.getRegistry('dcsys')
        self.host = registry.get('host')
        self.db = registry.get('database')
        self.user = registry.get('user')
        self.passw = registry.get('password')


    def _connect(self):
        con = psycopg2.connect(host=self.host, dbname=self.db, user=self.user, password=self.passw, cursor_factory=DictCursor)
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
                offices_temp = Office.findById(con, ['45cc065a-7033-4f00-9b19-d7d097129db3'])
                assert len(offices_temp) == 1
                office = offices_temp[0]

                logging.info('transformando logs al formato del sistema')
                tlogs = []
                for l in logs:
                    logging.debug(l)

                    dni = l['PIN']
                    userData = User.findUserByDni(con, dni)
                    userId = None
                    if userData is None:
                        (userId, version) = userData
                        user = User()
                        user.id = userId
                        user.dni = l['PIN']
                        user.name = 'autogenerado asistencia'
                        user.lastname = 'autogenerado asistencia'
                        user.persist(con)

                        ''' agrego la persona a la oficina de asistencia autogenerados - el id esta en insert_basic_data.sql '''
                        office.appendUser(userId)
                        office.persist(con)

                    else:
                        (userId, version) = userData

                    date = l['DateTime']
                    aware = Utils.localize(self.timezone, date)
                    utcaware = Utils.awareToUtc(aware)

                    log = Log()
                    log.id = str(uuid.uuid4())
                    log.userId = userId
                    log.deviceId = self.deviceId
                    log.verifyMode = l['Verified']
                    log.log = utcaware
                    tlogs.append(log)

                logging.info('salvando logs en la base')
                for l in tlogs:
                    logging.debug(l)
                    l.persist(con)

                con.commit()


                """ borro los logs del reloj """
                nowdate = datetime.datetime.now()
                deletestart = nowdate.replace(hour=int(self.hour_start_delete), minute=int(self.minute_start_delete), second=0, microsecond=0)
                deleteend = nowdate.replace(hour=int(self.hour_end_delete), minute=int(self.minute_end_delete), second=0, microsecond=0)
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
                            #self.zk.clearAttLogs()

            finally:
                con.close()

        except Exception as e:
            logging.exception(e)




def _sincLogs(main):
    main.sincLogs()


def config_injector(binder):
    pass


if __name__ == '__main__':

    """
    if len(sys.argv) <= 1:
        print('Debe pasar como parámetro la ip del reloj y el puerto.')
        print('Ej:')
        print('python ' + sys.argv[0] + ' 127.0.0.1 8080')
        sys.exit(1)
    """

    logging.basicConfig(filename='/var/log/firmware-sync.log',format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

    logging.info('Iniciando el sincronizador de logs')

    main = Main()
    rt = Periodic(main.period, _sincLogs, main)

    def close_sig_handler(signal,frame):
        logging.info('Cerrando sistema sincronizador')
        rt.stop()
        sys.exit()

    signal.signal(signal.SIGINT,close_sig_handler)

    while True:
        time.sleep(1000)
