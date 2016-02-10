# -*- coding: utf-8 -*-
import uuid, datetime,psycopg2,inject, math
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
            size real NOT NULL,
            file_name VARCHAR,
            camera_id VARCHAR REFERENCES camera.camera (id),
            duration VARCHAR
          );
    '''

    def _convertSizeUnit(self,size):
        if size < 1024:
            return str(size)
        elif size < (math.pow(1024, 2)):
            return "%3.1f%s" % (size/1024, ' KB')
        elif size < (math.pow(1024, 3)):
            return "%3.1f%s" % (size/(math.pow(1024, 2)), ' MB')
        elif size < (math.pow(1024, 4)):
            return "%3.1f%s" % (size/(math.pow(1024, 3)), ' GB')
        elif size < (math.pow(1024, 5)):
            return "%3.1f%s" % (size/(math.pow(1024, 4)), ' TB')
        return str(size)


    def _convertRecordingToDict(self,rec,camera):
        displayName = str(camera['number']) + ' - ' + camera['floor']
        start = rec[3]
        end = rec[4]
        sizeStr = self._convertSizeUnit(rec[5])
        return {'id':rec[0],'displayName':displayName,'start':start,'end':end,'size':rec[5],'duration':rec[8],'fileName':rec[6],'src':rec[2],'fps':str(rec[1]),'camera':camera,'sizeStr':sizeStr}


    def findRecordings(self,con,start,end,cameras):
        cur = con.cursor()
        if cameras is None or len(cameras) == 0:
            cur.execute('SELECT id,fps,source,start,rend,size,file_name,camera_id,duration FROM camera.recording WHERE start >= %s and rend <= %s',(start,end))
        else:
            cur.execute('SELECT id,fps,source,start,rend,size,file_name,camera_id,duration FROM camera.recording WHERE start >= %s and rend <= %s and camera_id in %s',(start,end,(tuple(cameras,))))
        if cur.rowcount <= 0:
            return []
        recordings = []
        for r in cur:
            camera = self.findCamera(con,r[7])
            recordings.append(self._convertRecordingToDict(r,camera))

        return recordings

    def deleteAllRecordings(self,con):
        cur = con.cursor()
        cur.execute('delete from camera.recording')

    def persistCamera(self,con,rec):
        if rec is None:
            return

        # precondiciones
        if 'start' not in rec or rec['start'] is None or 'rend' not in rec or rec['rend'] is None:
            return

        start = rec['start']
        if self.date.isNaive(start):
            ldate = self.date.localizeLocal(start)
            start = self.date.awareToUtc(ldate)
        else:
            start = self.date.awareToUtc(rec['start'])

        end = rec['rend']
        if self.date.isNaive(end):
            ldate = self.date.localizeLocal(end)
            end = self.date.awareToUtc(ldate)
        else:
            end = self.date.awareToUtc(rec['rend'])

        params = (rec['fps'] if 'fps' in rec else None,
                  rec['source'] if 'source' in rec else None,
                  start,
                  end,
                  rec['size'] if 'size' in rec else 0,
                  rec['file_name'] if 'file_name' in rec else None,
                  rec['camera_id'] if 'camera_id' in rec else None,
                  rec['duration'] if 'duration' in rec else '00:00:00',
                 )

        cur = con.cursor()
        cur.execute('set timezone to %s',('UTC',))

        if 'id' not in rec or rec['id'] is None:
            id = str(uuid.uuid4())
            params = params + (id,)
            cur.execute('insert into camera.recording (fps,source,start,rend,size,file_name,camera_id,duration,id) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)',params)
        else:
            params = params + (rec['id'],)
            cur.execute('update camera.recording set fps = %s, source = %s, start = %s, rend = %s, size = %s, file_name = %s, camera_id = %s, duration = %s  where id = %s',params)
