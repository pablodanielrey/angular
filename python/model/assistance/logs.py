# -*- coding: utf-8 -*-
import datetime, pytz
import json, logging
import inject
import itertools

from model import utils
from model.assistance.date import Date
from model.assistance.devices import Devices
from model.users.users import UserDAO

class Logs:

    date = inject.attr(Date)
    devices = inject.attr(Devices)


    def _convertToDict(self,data):
        d = {}
        d['id'] = data[0]
        d['deviceId'] = data[1]
        d['userId'] = data[2]
        d['verifymode'] = data[3]
        d['log'] = data[4]
        return d


    ''' Busca el log por el id '''
    def findLog(self,con,id):
        cur = con.cursor()
        cur.execute('select id,device_id,user_id,verifymode,log from assistance.attlog where id = %s',(id,))
        d = cur.fetchone()
        if d:
            return self._convertToDict(d)
        else:
            return None


    '''
        busca un log por una fecha determinada. la fecha debe estar en utc y ser aware
    '''
    def findLogByDate(self,con,date):
        cur = con.cursor()
        cur.execute('select id,device_id,user_id,verifymode,log from assistance.attlog where log = %s',(date,))
        if cur.rowcount <= 0:
            return None
        return self._convertToDict(cur.fetchone())



    '''
        obtiene los logs
        dfrom y dto deben estar en UTC
    '''
    def findLogs(self,con,userId,dfrom=None,dto=None):
        cur = con.cursor()
        cur.execute("set timezone to 'UTC'")

        if dfrom == None and dto == None:
            cur.execute('select id,device_id,user_id,verifymode,log from assistance.attlog where user_id = %s ORDER BY log', (userId,))

        elif dfrom == None:
            if self.date.isNaive(dfrom):
                raise TypeError('dfrom is naive')
            cur.execute('select id,device_id,user_id,verifymode,log from assistance.attlog where user_id = %s and log <= %s ORDER BY log',(userId,dto))

        elif dto == None:
            if self.date.isNaive(dto):
                raise TypeError('dto is naive')
            cur.execute('select id,device_id,user_id,verifymode,log from assistance.attlog where user_id = %s and log >= %s ORDER BY log',(userId,dfrom))

        elif dfrom is not None and dto is not None:
            cur.execute('select id,device_id,user_id,verifymode,log from assistance.attlog where user_id = %s and log >= %s and log <= %s ORDER BY log',(userId,dfrom,dto))

        if cur.rowcount <= 0:
            return []

        #data = cur.fetchall()
        logs = []
        for d in cur:
            logs.append(self._convertToDict(d))
        return logs




    ''' persiste el log solo si no existe algun log con ese id '''
    def persist(self,con,data):
        params = (data['id'],data['deviceId'],data['userId'],data['verifymode'],data['log'])
        cur = con.cursor()
        cur.execute('set time zone %s',('utc',))
        cur.execute('insert into assistance.attlog (id,device_id,user_id,verifymode,log) values (%s,%s,%s,%s,%s)',params)


    '''
        Persiste los logs que no existan en la base pasados como parámetro
        retorna:
            Lista de logs sincronizados
    '''
    def persistLogs(self,con,logs):
        lenLogs = len(logs)
        if lenLogs <= 0:
            return []

        ids = [l['id'] for l in logs]
        cur = con.cursor()
        cur.execute('select id from assistance.attlog where id in %s',(tuple(ids),))
        if cur.rowcount == lenLogs:
            logging.debug('Ya existen todos los logs enviados dentro de la base')
            return []

        logsToRemove = []
        if cur.rowcount > 0:
            logsToRemove = [l[0] for l in cur.fetchall()]
        logging.debug('ya existen estos logs {}'.format(logsToRemove))

        logsToSync = [l for l in logs if l['id'] not in logsToRemove]
        logging.debug('logs a sincronizar {}'.format(logsToSync))

        cur.execute('set time zone %s',('utc',))
        for l in logsToSync:
            params = (l['id'],l['deviceId'],l['userId'],l['verifymode'],l['log'])
            cur.execute('insert into assistance.attlog (id,device_id,user_id,verifymode,log) values (%s,%s,%s,%s,%s)',params)

        return logsToSync



    ''' a partir de una lista de datetime obtiene los grupos de worked '''
    def _getWorkedTimetable(self, dateList):
        worked = []
        bytwo = list(utils.grouper(2,dateList))
        #logging.debug(bytwo)
        for s,e in bytwo:
            w = {
                'start':s,
                'end':e,
                'seconds':(e-s).total_seconds() if s is not None and e is not None and s <= e else 0
            }
            worked.append(w)
        return worked


    ''' controlo la tolerancia entre logs -- 5 minutos '''
    def _checkTolerance(self, log):
        if self._dateBefore == None:
            self._dateBefore = log
            return True

        ret = (log - self._dateBefore) >  datetime.timedelta(minutes=5)
        self._dateBefore = log
        return ret


    '''
        Retorna el conjunto de horas trabajadas de a pares despues de chequear la tolerancia de las marcas.
        tambien retonra el conjunto válido de logs tomados para realizar el cálculo
    '''
    def getWorkedHours(self, logs):
        attlogs = list(map(lambda e : e['log'] , logs))

        self._dateBefore = None
        attlogs = list(filter(self._checkTolerance,attlogs))

        worked = self._getWorkedTimetable(attlogs);
        return (worked,attlogs)


    '''
        Procesa el conjunto de horas trabajadas y retorna.
        (
            Hora inical del trabajo
            Hora final completa del trabajo
            Cantidad de segundos trabajados en total
        )
    '''
    def explainWorkedHours(self,whs):
        sdate = None
        edate = None
        totalSeconds = 0

        if len(whs) > 0:
            sdate = whs[0]['start']
            edate = whs[-1]['end']
            totalSeconds = 0
            for w in whs:
                totalSeconds = totalSeconds + w['seconds']

        return (sdate,edate,totalSeconds)








    '''
    transforma el mensaje en json obtenido desde el firware a log

    Todas las fechas que se manejan en el modelo son UTC.
    si se obtienen desde lugares en localtime se convierten a utc para ser trabajadas.

    formato del log enviado y recibido mediante json

    {
        "id":"03050f03-ff1a-427e-959e-9937a97b9392",
        "device":{
            "id":"1bb8258e-d3e4-4c29-9c4f-354c881668b8",
            "name":"zk1",
            "description":"dispositivo ZK 1",
            "ip":"163.10.56.29",
            "netmask":"255.255.255.192",
            "enabled":true
        },
        "person":{
            "id":"c4ac0f86-726f-44b6-bb4c-f809e78607d3",
            "name":"Usuario",
            "lastName":"Nuevo",
            "dni":"28869650",
            "gender":"M",
            "types":[],
            "telephones":[]
        },
        "date":"08:04:08 13/03/2015",
        "verifyMode":1
    }

    '''
    def fromJsonMessage(self,con,jsonLog):
        fullLog = json.loads(jsonLog)

        person = fullLog['person']
        dni = person['dni']
        user = UserDAO.findUserByDni(con,dni)
        personId = user['id']

        device = fullLog['device']
        devId = device['id']

        ''' TODO: obtengo la zona del dispositivo. MEJORAR!!! '''
        timezone = self.devices.getTimeZone(devId)

        ''' transformo la fecha obtenida desde el firmware a utc '''
        date = datetime.datetime.strptime(fullLog['date'], "%H:%M:%S %d/%m/%Y")
        local = self.date.localize(timezone,date)
        utcdate = self.date.awareToUtc(local)


        log = {}
        log['id'] = fullLog['id']
        log['deviceId'] = devId
        log['userId'] = personId
        log['verifymode'] = fullLog['verifyMode']
        log['log'] = utcdate

        return log
