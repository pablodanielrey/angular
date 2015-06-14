# -*- coding: utf-8 -*-


class Devices:

    def getTimeZone(self,con,id):
        cur = con.cursor()
        cur.execute('select timezone from assistance.devices where id = %s',(id,))
        if cur.rowcount <= 0:
            return "America/Buenos_Aires"
        return cur.fetchone()[0]


    def persist(self,con,device):

        timezone = 'America/Buenos_Aires'
        if 'timezone' in device:
            timezone = device['timezone']

        req = (device['id'],device['device'],device['ip'],device['enabled'],timezone)
        cur = con.cursor()
        cur.execute('insert into assistance.devices (id,device,ip,enabled,timezone) values (%s,%s,%s,%s,%s)',req)
