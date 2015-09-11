# -*- coding: utf-8 -*-
import uuid, datetime,psycopg2,inject
from model.systems.assistance.date import Date

class Camaras:

    date = inject.attr(Date)


    def findAllCamaras(self,con):
        return []


    def findRecordings(self,con,start,end,camaras):
        recordings = []
        r1 = {'displayName':'1 - Planta Baja','start':self.date.now(),'duration':'01:25:13','size':'45 Mb','fileName':'2015-07-31_23-00-02','src':'http://163.10.56.194/gluster/camaras/archivo/2015-08-18_09-00-01_camara1.m4v.mp4'}
        recordings.append(r1)
        return recordings
