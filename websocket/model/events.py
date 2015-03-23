# -*- coding: utf-8 -*-
import json

"""
    Módulo que soporta el envío de eventos y mensajes
    hacia el lado cliente y locales


    Los mensajes enviados al lado cliente son de la forma :

    {
        type: 'tipo de evento enviado'
        data: 'datos del mensaje (estos dependen del evento)'
    }

"""




class Events:

    def __init__(self):
        self.listeners = [];

    def addListener(self,l):
        self.listeners.append(l);

    def removeListener(self,l):
        self.listeners.remove(l)

    def broadcastLocal(self,msg):
        for l in self.listeners:
            l.event(msg)

    def broadcast(self,server,msg):
        self.broadcastLocal(msg)
        self.broadcastRemote(server,msg)

    def broadcastRemote(self,server,msg):
        for c in server.server.connections.values():
          c.sendMessage(msg)
