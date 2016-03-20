# -*- coding: utf-8 -*-
import uuid, datetime,psycopg2

class Task:

    def getTasks(self,con,userId):
        cur = con.cursor()
        cur.execute('select id, description, user_id, finish, created from task.task where user_id = %s',(userId,))
        tasks = []
        for task in cur.fetchall():
            tasks.append(self._convertToDict(task))
        return tasks

    def _convertToDict(self,task):
        return {'id':task[0],'text':task[1],'userId':task[2],'finish':task[3],'created':task[4]}

    def find(self,con,id):
        cur = con.cursor()
        cur.execute('select id, description, user_id, finish, created from task.task where id = %s',(id,))
        if cur.rowcount <= 0:
            return None
        return self._convertToDict(cur.fetchone())


    def findByStatus(self,con,userId,status):
        cur = con.cursor()
        params = [userId,status]
        cur.execute('select id, description, user_id, finish, created from task.task where user_id = %s and finish = %s',params)
        tasks = []
        for task in cur.fetchall():
            tasks.append(self._convertToDict(task))
        return tasks


    def createTask(self,con,userId,text):
        cur = con.cursor()
        id = str(uuid.uuid4())
        finish = False
        params = [id,text,userId,finish]
        cur.execute('insert into task.task (id,description,user_id,finish) values(%s,%s,%s,%s)',params)
        return id


    def updateStatus(self,con,taskId,status):
        cur = con.cursor()
        params = [status,taskId]
        cur.execute('update task.task set finish = %s where id = %s',params)
        return taskId


    def removeTask(self,con,taskId):
        cur = con.cursor()
        cur.execute('delete from task.task where id = %s',(taskId,))
        return taskId

    def removeTaskByStatus(self,con,userId,status):
        tasks = self.findByStatus(con,userId,status)
        ids = []
        for t in tasks:
            id = self.removeTask(con,t["id"])
            ids.append(id)
        return ids
