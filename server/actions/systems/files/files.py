# -*- coding: utf-8 -*-
import inject
import logging

import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession

from model.registry import Registry
from model.connection.connection import Connection
from model.files.files import FileDAO, File


class FilesWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)

        r = inject.instance(Registry)
        self.conn = Connection(r.getRegistry('dcsys'))
        self.files = inject.instance(FileDAO)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.find_async, 'system.files.find')
        yield from self.register(self.findById_async, 'system.files.findMetaDataById')
        yield from self.register(self.upload_async, 'system.files.upload')
        yield from self.register(self.findAllIds, 'system.files.findAllIds')

    def findAllIds(self):
        con = self.conn.get()
        try:
            r = self.files.findAll(con)
            return r

        finally:
            self.conn.put(con)

    def find(self, id):
        con = self.conn.get()
        try:
            r = self.files.findById(con, id)
            r.content = self.files.getContent(con, id)
            rs = r.__dict__
            return rs

        finally:
            self.conn.put(con)

    def findById(self, id):
        con = self.conn.get()
        try:
            r = self.files.findById(con, id)
            rs = r.__dict__
            return rs

        finally:
            self.conn.put(con)

    def upload(self, id, name, mimetype, codec, data):
        con = self.conn.get()
        try:
            f = File()
            f.name = name
            f.mimetype = mimetype
            f.codec = codec
            f.size = len(data)
            f._calculateHash()

            id = self.files.persist(con, f)
            con.commit()
            return id

        finally:
            self.conn.put(con)

    @coroutine
    def upload_async(self, id, name, mimetype, codec, data):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.upload, id, name, mimetype, codec, data)
        return r

    @coroutine
    def find_async(self, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.find, id)
        return r

    @coroutine
    def findMetaDataById_async(self, id):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findMetaDataById, id)
        return r
