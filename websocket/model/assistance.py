# -*- coding: utf-8 -*-
from Ws.SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
from websocket import create_connection
import json, base64
import datetime
import traceback
import logging
from wexceptions import MalformedMessage
from model.profiles import AccessDenied
from model.utils import DateTimeEncoder


class AssistanceWebSocketClient():

    def handle(self,config):
        print "ws://"+config.configs['websocketClient_ip']+":"+config.configs['websocketClient_port']+"/websocket"
        #ws = create_connection("ws://"+config.configs['websocketClient_ip']+":"+config.configs['websocketClient_port']+"/websocket")
        ws = create_connection("wss://echo.websocket.org")

        print ws
        print "Sending 'Hello, World'..."
        ws.send("Hello, World")
        print "Sent"
        print "Reeiving..."
        result =  ws.recv()
        print "Received '%s'" % result
        ws.close()


class AssistanceWebsocketServer(WebSocket):

  def setActions(self,actions):
    self.actions = actions

  def sendException(self,e):
      msg = {'type':'Exception','name':e.__class__.__name__}
      self.sendMessage(msg)

  def sendError(self,msg,e):
      mmsg = {'id':msg['id'],'error':e.__class__.__name__}
      self.sendMessage(mmsg)

  def handleMessage(self):
    try:

      if self.data is None:
        raise NullData()

      """
      self.data ->
      attLog;{"id":"03050f03-ff1a-427e-959e-9937a97b9392",
             "device":{"id":"1bb8258e-d3e4-4c29-9c4f-354c881668b8","name":"zk1","description":"dispositivo ZK 1","ip":"163.10.56.29","netmask":"255.255.255.192","enabled":true},
             "person":{"id":"c4ac0f86-726f-44b6-bb4c-f809e78607d3","name":"Usuario","lastName":"Nuevo","dni":"28869650","gender":"M","types":[],"telephones":[]},
             "date":"08:04:08 13/03/2015",
             "verifyMode":1}

      """

      cmdLog = "attLog;"
      if not(self.data.startswith(cmdLog)):
          return


      msgStr = self.data[len(cmdLog):]


      """ decodifico el log """

      message = json.loads(msgStr.decode('utf-8'))

      obj = message['id']
      print "Id log:"+obj
      person = message['person']
      print "DNI:"+ person['dni']

      #jmsg = json.dumps(msg,cls=DateTimeEncoder)

      #logging.debug("lalalalaaaaaaaaaaa");

      #super(WebsocketServer,self).sendMessage("{OK;}");

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
