# -*- coding: utf-8 -*-
import uuid, datetime,psycopg2,inject
from model.systems.assistance.date import Date

class Camaras:

    date = inject.attr(Date)

    # -----------------------------------------------------------------------------------
    # ---------------------------- CAMARAS ----------------------------------------------
    # -----------------------------------------------------------------------------------

    '''
          CREATE TABLE camera.camera (
            id VARCHAR NOT NULL PRIMARY KEY,
            mac VARCHAR,
            ip VARCHAR,
            floor VARCHAR,
            number INTEGER
          );
    '''

    def _convertCameraToDict(self,c):
        return {'id':c[0],'mac':c[1],'ip':c[2],'floor':c[3],'number':c[4]}

    def findAllCameras(self,con):
        cur = con.cursor()
        cur.execute('select id, mac, ip, floor, number from camera.camera')
        if cur.rowcount <= 0:
            return []
        cameras = []
        for c in cur:
            cameras.append(self._convertCameraToDict(c))
        return cameras

    def findCamera(self,con,id):
        cur = con.cursor()
        cur.execute('select id, mac, ip, floor, number from camera.camera where id = %s',(id,))
        if cur.rowcount <= 0:
            return None
        return self._convertCameraToDict(cur.fetchone())


    # -----------------------------------------------------------------------------------
    # ---------------------------- ARCHIVOS ---------------------------------------------
    # -----------------------------------------------------------------------------------
    '''
          CREATE TABLE camera.recording (
            id VARCHAR NOT NULL PRIMARY KEY,
            fps decimal,
            source VARCHAR,
            start timestamptz NOT NULL,
            rend timestamptz NOT NULL,
            size VARCHAR NOT NULL,
            file_name VARCHAR,
            camera_id VARCHAR REFERENCES camera.camera (id)
          );
    '''

    def _convertRecordingToDict(self,rec,camera):
        displayName = camera['number'] + ' - ' + camera['floor']
        start = rec[3]
        end = rec[4]
        duration = end - start
        return {'id':rec[0],'displayName':displayName,'start':start,'end':end,'size':rec[5],'duration':duration,'fileName':rec[6],'src':rec[2],'fps':rec[1],'camera':camera}


    def findRecordings(self,con,start,end,cameras):
        cur = con.cursor()
        if cameras is None or len(cameras) == 0:
            cur.execute('SELECT id,fps,source,start,rend,size,file_name,camera_id FROM camera.recording WHERE start >= %s and rend <= %s',(start,end))
        else:
            cur.execute('SELECT id,fps,source,start,rend,size,file_name,camera_id FROM camera.recording WHERE start >= %s and rend <= %s and camera_id in %s',(start,end,cameras))
        if cur.rowcount <= 0:
            return []
        recordings = []
        for r in cur:
            camera = self.findCamera(con,r[7])
            recordings.append(self._convertRecordingToDict(r,camera))
        return recordings
