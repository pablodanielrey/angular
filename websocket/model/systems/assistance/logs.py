# -*- coding: utf-8 -*-

"""
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

"""

import datetime, pytz
import json

from model.systems.assistance.date import Date
from model.systems.assistance.devices import Devices


class Logs:

    date = inject.attr(Date)
    users = inject.attr(Users)
    devices = inject.attr(Devices)


    def _convertToDict(self,data):
        d = {}
        d['id'] = data[0]
        d['deviceId'] = data[1]
        d['userId'] = data[2]
        d['verifymode'] = data[3]
        d['log'] = data[4]
        return d


    """ Busca el log por el id """
    def findLog(self,con,id):
        cur = con.cursor()
        cur.execute('select id,device_id,user_id,verifymode,log from assistance.attlog where id = %s',(id,))
        d = cur.fetchone()
        if d:
            return self._convertToDict(d)
        else:
            return None


    """ obtiene los logs de una fecha utc en paticular """
    def findLogs(self,con,userId,date):
        cur = con.cursor()
        cur.execute('select id,device_id,user_id,verifymode,log from assistance.attlog where user_id = %s and log::date = %s::date',(userId,date))
        data = cur.fetchall()
        logs = []
        for d in data:
            logs.append(self._convertToDict(d))
        return logs


    """ persiste el log solo si no existe algun log con ese id """
    def persist(self,con,data):
        if (self.findLog(con,data['id'])) == None:
            params = (data['id'],data['deviceId'],data['userId'],data['verifymode'],data['log'])
            cur = con.cursor()
            cur.execute('insert into assistance.attlog (id,device_id,user_id,verifymode,log) values (%s,%s,%s,%s,%s)',params)


    """ transforma el mensaje en json obtenido desde el firware a log """
    def fromJsonMessage(self,con,jsonLog):
        fullLog = json.loads(msgStr.decode('utf-8'))

        person = fullLog['person']
        dni = person['dni']
        user = self.users.findUserByDni(con,dni)
        personId = user['id']

        device = fullLog['device']
        devId = device['id']

        """ TODO: obtengo la zona del dispositivo. MEJORAR!!! """
        timezone = self.devices.getTimeZone(deviceId)


        """ transformo la fecha obtenida desde el firmware a utc """
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
