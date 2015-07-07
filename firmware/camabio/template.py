# -*- coding: utf-8 -*-
import codecs, logging
import inject, uuid

from model.config import Config
from model.systems.assistance import templates

class Templates:

    config = inject.attr(Config)
    templates = inject.attr(templates.Templates)

    def __generate_template(self,userId,number,template):
        id = str(uuid.uuid4())
        mapping = {
            'number':number,
            'id': id,
            'userId': userId
        }
        tmpl = {
            'id': id,
            'template':template,
            'algorithm':self.config.configs['reader_algorithm'],
            'userId':userId
        }
        return (mapping,tmpl)


    def __persist(self,conn,mapping):
        req = (mapping['id'],mapping['userId'],mapping['number'])
        cur = conn.cursor()
        cur.execute('delete from assistance.template_mapping where template_id = %s and user_id = %s and reader_index = %s',req)
        cur.execute('insert into assistance.template_mapping (template_id,user_id,reader_index) values (%s,%s,%s)',req)

    def persist(self,conn,userId,number,template):
        (mapping,tmpl) = self.__generate_template(userId,number,template)
        self.templates.persist(conn,tmpl)
        self.__persist(conn,mapping)


    def findUserIdByIndex(self,conn,number):
        cur = conn.cursor()
        cur.execute('select user_id from assistance.template_mapping where number = %s',(number,))
        if cur.rowcount <= 0:
            return None
        return cur.fetchone()[0]
