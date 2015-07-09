# -*- coding: utf-8 -*-


class Devices:

    def getTimeZone(self,con,id):
        cur = con.cursor()
        cur.execute('select timezone from assistance.devices where id = %s',(id,))
        if cur.rowcount <= 0:
            return "America/Buenos_Aires"
        return cur.fetchone()[0]


    def _getTimeZone(self,device):
        timezone = 'America/Buenos_Aires'
        if 'timezone' in device:
            timezone = device['timezone']
        return timezone


    def persist(self,con,device):
        timezone = self._getTimeZone(device)

        req = (device['id'],device['device'],device['ip'],device['enabled'],timezone, datetime.datetime.now())
        cur = con.cursor()
        cur.execute('insert into assistance.devices (id,device,ip,enabled,timezone,created) values (%s,%s,%s,%s,%s,%s)',req)


    def update(self,con,device):
        timezone = self._getTimeZone(device)

        req = (device['id'],device['device'],device['ip'],device['enabled'],timezone, datetime.datetime.now())
        cur = con.cursor()
        cur.execute('insert into assistance.devices (id,device,ip,enabled,timezone,created) values (%s,%s,%s,%s,%s,%s)',req)


    def find(self,con,id):
        cur = con.cursor()
        cur.execute('select id,device,ip,enabled,timezone where id = %s',(id,))
        if (cur.rowcount <= 0):
            return None
        else:
            return cur.fetchone()


    def persistOrUpdate(self,con,device):
        d = self.find(con,device[id])
        if d:
            self.update(con,device)
        else:
            self.persist(con,device)
