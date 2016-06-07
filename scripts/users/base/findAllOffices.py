# -*- coding: utf-8 -*-
import connection
import groups
import logging
from pprint import pprint

if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)
    con = connection.getConnection()
    try:
        for oid in groups.OfficeDAO.findAll(con):
            office = groups.OfficeDAO.findById(con, oid)
            pprint(office.__dict__)

    finally:
        connection.closeConnection(con)
