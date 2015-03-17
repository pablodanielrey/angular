# -*- coding: utf-8 -*-
from Ws.SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
import json, base64
import datetime
import traceback
import logging
from wexceptions import MalformedMessage
from model.profiles import AccessDenied
from model.utils import DateTimeEncoder


class AssistanceWebsocketServer(WebSocket):


  def handleMessage(self):
    try:
      if self.data is None:
        raise NullData()

      print 'C:' + self.data
      message = json.loads(str(self.data))

      """ decodifico el log """

      jmsg = json.dumps(msg,cls=DateTimeEncoder)

      logging.debug("lalalalaaaaaaaaaaa");

      super(WebsocketServer,self).sendMessage("{OK;}");

    except Exception as e:
      print e.__class__.__name__ + ' ' + str(e)
      """
      traceback.print_exc()
      self.sendException(e)
      """



  def handleConnected(self):
    print("connected : ",self.address)

  def handleClose(self):
    print("closed : ",self.address)





class Asssistance:

    """ http://stackoverflow.com/questions/4998427/how-to-group-elements-in-python-by-n-elements """
    def _grouper(n, iterable, fillvalue=None):
        "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
        args = [iter(iterable)] * n
        return izip_longest(fillvalue=fillvalue, *args)


    """ a partir de una lista de datetime obtiene los grupos de worked """
    def _getWorkedTimetable(self, logList):
        worked = []
        bytwo = _grouper(2,logList)
        for b in bytwo:
            w = { 'start':b[0], 'end':b[1], 'minutes':(b[1]-b[0]).total_seconds() }
            worked.append(w)
        return worked


    """ obtiene el estado de asistencia del dia actual del usuario """
    def getAssistanceStatus(self,con,userId):

        date = new Date()
        logs = self._getLogs(con,userId,date)
        attlogs = map(function(e) { return e['date'] }, logs)
        inside = len(attlogs) % 2
        worked = self._getWorkedTimetable(attlogs);
        sdate = worked[0]['start']
        edate = worked[-1]['end']
        totalMinutes = 0
        for w in worked:
            totalMinutes = totalMinutes + w['minutes']

        assistanceStatus = {
            'status': inside,
            'start': sdate,
            'end': edate,
            'logs': attlogs,
            'workedMinutes': totalMinutes
        }
        return assistanceStatus



    """ obtiene los logs de una fecha en paticular """
    def _getLogs(self,con,userId,date):
        cur = con.cursor()
        cur.execute('select device_id, user_id, verifymode, date from assistance.attlog where user_id = %s and date::date = %s::date',(userId,date))
        data = cur.fetchall()
        logs = []
        for d in data:
            logs.append(self._convertToDict(d))
        return logs


    def _convertToDict(self,data):
        d['deviceId'] = data[0]
        d['userId'] = data[1]
        d['verifymode'] = data[2]
        d['date'] = data[3]
