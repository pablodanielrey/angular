# -*- coding: utf-8 -*-
import codecs, logging
import psycopg2
from reader import FirmwareReader

class Firmware:

    def need_first(self):
        logging.info('1')

    def need_second(self):
        logging.info('2')

    def need_third(self):
        logging.info('3')

    def need_release(self):
        logging.info('r')



    def __init__(self,port):
        self.reader = FirmwareReader(port)
        self.conn = None

    def __get_database__(self):
        return psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])


    def start(self):
        self.reader.start()
        self.conn = self.__get_database__()


    def stop(self):
        self.reader.stop()
        if self.conn:
            self.conn.close()

    def enroll(self,pin):
        (n,t) = self.reader.enroll(self.need_first,self.need_second,self.need_third,self.need_release)
        if n:
            """ se tiene la huella con el id, hay que asignarle le usuario """
            userId = None
            user = self.users.findUserByDni(self.conn,pin)
            if not user:
                user = {
                    'dni':pin,
                    'name':'autorgenerado',
                    'lastname':'autogenerado'
                }
                userId = self.users.createUser(self.conn,user)
            else:
                userId = user['id']

            self.templates.


    def identify(self):
        h = self.reader.identify()
