
from model.registry import Registry
from model.connection.connection import Connection
from model.laboralinsertion.inscription import Inscription
from model.users.users import User, UserDAO
import model.laboralinsertion.user

from model.files.files import File

import PyPDF2
import base64
import inject
import logging
from io import BytesIO

if __name__ == '__main__':

    logging.getLogger().setLevel(logging.WARNING)
    #inject.configure()
    conn = Connection(inject.instance(Registry).getRegistry('dcsys'))
    con = conn.get()
    try:

        uids = set([ i.userId for i in Inscription.findById(con, Inscription.findAll(con)) ])
        for i in uids:
            logging.warn('chequeando cv de : {}'.format(i))
            usr = UserDAO.findById(con, [i])[0]
            cvi = model.laboralinsertion.user.User.findById(con, i)[0].cv

            try:
                content = base64.b64decode(File.getContentById(con, cvi))

                fn = '/tmp/insercion/{}.pdf'.format(cvi)
                with open(fn, 'wb') as f:
                    f.write(content)

                with BytesIO(content) as buff:
                    try:
                        logging.warn('comenzando a leer el pdf')
                        PyPDF2.PdfFileReader(buff)
                        logging.warn('{} {} {} {} ok'.format(usr.dni, usr.name, usr.lastname, cvi))
                        import os
                        os.remove(fn)

                    except PyPDF2.utils.PdfReadError:
                        logging.warn('El usuario {} {} {} {} tiene el cv {} sin formato pdf'.format(i, usr.dni, usr.name, usr.lastname, cvi))

            except Exception as e:
                logging.warn('El usuario {} {} {} {} tiene error en el cv {}'.format(i, usr.dni, usr.name, usr.lastname, cvi))

    finally:
        conn.put(con)
