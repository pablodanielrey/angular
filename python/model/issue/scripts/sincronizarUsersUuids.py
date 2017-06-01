
import psycopg2
import os
import logging

if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)
    roots_procesed = set()

    con = psycopg2.connect(
                    host=os.environ['DB_REDMINE_HOST'],
                    dbname=os.environ['DB_REDMINE_NAME'],
                    user=os.environ['DB_REDMINE_USER'],
                    password=os.environ['DB_REDMINE_PASSWORD'])
    try:
        cur = con.cursor()
        try:
            logging.info('buscando attachs')
            cur.execute('select container_id from attachments where container_type = %s', ('Issue',))
            for r in cur.fetchall():
                cont_id = r[0]
                root_id = None

                logging.info('attach {}'.format(cont_id))

                if cont_id in roots_procesed:
                    continue

                """ busco hasta llegar a la raiz """
                trans_id = cont_id
                ident = ' '
                while True:
                    logging.info('{} procesando : {}'.format(ident, trans_id))

                    cur.execute('select id, parent_id from issues where id = %s', (trans_id,))
                    if cur.rowcount <= 0:
                        break;
                    container = cur.fetchall()[0]
                    if container[1] == None:
                        root_id = container[0]
                        break;
                    else:
                        trans_id = container[1]

                    ident = ident + '  '

                if root_id and cont_id != root_id:
                    cur.execute('update attachments set container_id = %s where container_id = %s', (root_id, cont_id))
                    con.commit()
                    roots_procesed.add(root_id)

        finally:
            cur.close()
    finally:
        con.close()
