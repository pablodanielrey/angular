# -*- coding: utf-8 -*-
import ldap3
import psycopg2
import datetime, pytz
import sys, logging


"""
mapeos de justificaciones.
"""
jm = {
    '3942e050-cc2f-498a-9692-fee07204c70f':'76bc064a-e8bf-4aa3-9f51-a3c4483a729a',
    '6ca99411-c3d0-41a4-9183-2a096917e8cd':'b80c8c0e-5311-4ad1-94a7-8d294888d770',
    '9221cef9-6ea0-4063-a21d-a92e1145aa20':'b70013e3-389a-46d4-8b98-8e4ab75335d0',
    '8c7505e9-47dc-4d51-81de-67870a4135fb':'e0dfcef6-98bb-4624-ae6c-960657a9a741',
    '11d77ce9-8fb7-4a29-87a5-a28a3048b00b':'c32eb2eb-882b-4905-8e8f-c03405cee727',
    '390953d0-d883-4c90-b273-cf37d2a7b96b':'fa64fdbd-31b0-42ab-af83-818b3cbecf46',
    '672da5a4-9904-4f0b-b434-e55a99aea21e':'0cd276aa-6d6b-4752-abe5-9258dbfd6f09',
    'e013eb55-f8ee-49e5-b506-48aec1ad3fe4':'70e0951f-d378-44fb-9c43-f402cbfc63c8',
    '60c1fcf7-2e1b-4714-85cb-62f7ae376ace':'f9baed8a-a803-4d7f-943e-35c436d5db46',
    '5afc97ef-9ece-42a2-a741-93aa0363110d':'a93d3af3-4079-4e93-a891-91d5d3145155',
    '4280c6cf-0439-47af-b27f-b1525366e8a6':'508a9b3a-e326-4b77-a103-3399cb65f82a',
    'd2aa38bc-74a5-448d-af9c-3aaee9557f5d':'50998530-10dd-4d68-8b4a-a4b7a87f3972',
    '214751d7-725f-497a-a11b-9b3d7d6a3426':'478a2e35-51b8-427a-986e-591a9ee449d8',
    '482abf5f-b1fa-4c1f-842a-99a0b3d63098':'b309ea53-217d-4d63-add5-80c47eb76820',
    '43c99658-32a6-4cf1-9a7e-f564742d1077':'5c548eab-b8fc-40be-bb85-ef53d594dca9',
    '02c2e2da-cf29-4a85-9b86-ee03a0b58973':'5ec903fb-ddaf-4b6c-a2e8-929c77d8256f',
    '8cfd4b92-3495-4e07-a721-df2ffbb87bed':'48773fd7-8502-4079-8ad5-963618abe725',
    '394e4b23-d497-48aa-b84f-fc88bf2c6202':'508a9b3a-e326-4b77-a103-3399cb65f82a',
    '199b28e7-add5-4296-ac81-1469d1e98697':'e8019f0e-5a70-4ef3-922c-7c70c2ce0f8b',
    '6b2c2b5c-9a64-4fb6-b1ad-33cd0bfe68d2':'3fb52f24-3eff-4ca2-8133-c7a3abfc7262',
    '3b96f509-febc-4c39-a538-b6afaff293fb':'3d486aa0-745a-4914-a46d-bc559853d367',
    'f27836dc-2ba4-4135-98b0-379bb74b5ef1':'4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb',
    '3b41c98d-cda4-4370-aaa3-225c6a623474':'cb2b4583-2f44-4db0-808c-4e36ee059efe'
}


def localice(date):
    if date.tzinfo is not None:
        return date
    timezone = "America/Buenos_Aires"
    tz = pytz.timezone(timezone)
    local = tz.localize(date)
    return local


def copyjusts(src,dst):

    dcur = dst.cursor()
    dcur.execute("set timezone to 'UTC'")

    csrc = src.cursor()
    csrc.execute('select id,justification_id,person_id,jstart from justificationdate order by jstart asc')

    if csrc.rowcount <= 0:
        return

    for jrid, jid, userId, jbegin in csrc:

        if jid = '0b9f73c1-6f9b-4dfa-a168-2512651316aa':
            """ es la de prueba, la ignoro """
            continue

        jbegin = localice(jbegin)

        """ realizo el mapeo a las nuestas """
        if jid in jm:
            jid = jm[jid]

        if jid == 'fa64fdbd-31b0-42ab-af83-818b3cbecf46':
            logging.warn('No se procesan las boletas de salida')
            continue

        dcur.execute('select id from profile.users where id = %s',(userId,))
        if dcur.rowcount <= 0:
            logging.warn('{}'.format(jrid))
            logging.warn('usuario {} no existe en el destino'.format(userId))
            continue

        dcur.execute('select justification_id from assistance.justifications_requests where jbegin = %s and user_id = %s',(jbegin,userId))
        if dcur.rowcount > 0:
            logging.warn('ya existe una justificacion para {} en la fecha {}'.format(userId,jbegin))
            continue

        logging.info('insertando justification {} en {} para {}'.format(jid,jbegin,userId))
        dcur.execute('insert into assistance.justifications_requests (id,user_id,justification_id,jbegin,requestor_id) values (%s,%s,%s,%s,%s)',(jrid,userId,jid,jbegin,'1'))

        ffecha2 = datetime.datetime.now()
        ffecha3 = ffecha2 + datetime.timedelta(seconds=5)

        dcur.execute('insert into assistance.justifications_requests_status (request_id,user_id,status,created) values (%s,%s,%s,%s)',(jrid,userId,'PENDING',ffecha2))
        dcur.execute('insert into assistance.justifications_requests_status (request_id,user_id,status,created) values (%s,%s,%s,%s)',(jrid,'1','APPROVED',ffecha3))



if __name__ == '__main__':

    if len(sys.argv) < 11:
        logging.info('faltan argumentos')
        logging.info('python3 {} host-db-origen port-db-origen db-origen-user db-origen-pass db-orgien host-db-destino port-db-destino db-user-destino db-pass-destino db-destino'.format(sys.argv[0]))
        sys.exit(1)

    shost = sys.argv[1]
    sport = sys.argv[2]
    suser = sys.argv[3]
    spassw = sys.argv[4]
    sdb = sys.argv[5]

    dhost = sys.argv[6]
    dport = sys.argv[7]
    duser = sys.argv[8]
    dpassw = sys.argv[9]
    ddb = sys.argv[10]

    #logging.basicConfig(filename='/tmp/copy-justs.log',format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

    logging.info('conectandose a las bases')
    src = psycopg2.connect(host=shost, port=sport, user=suser, password=spassw, dbname=sdb)
    dst = psycopg2.connect(host=dhost, port=dport, user=duser, password=dpassw, dbname=ddb)

    logging.info('copiando justificaciones')
    copyjusts(src,dst)

    dst.commit()

    src.close()
    dst.close()
