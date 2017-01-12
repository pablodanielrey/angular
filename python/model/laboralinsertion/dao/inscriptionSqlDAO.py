from model.dao import SqlDAO
from model.laboralinsertion.entities.company import Company
from model.laboralinsertion.entities.contact import Contact

class InscriptionSqlDAO(SqlDAO):

    _schema = "laboral_insertion."
    _table = "inscriptions"
    _entity = Inscription


@classmethod
def _createSchema(cls, ctx):
    super()._createSchema(ctx.con)
    cur = con.cursor()
    try:
        cur.execute("""
            CREATE SCHEMA IF NOT EXISTS laboral_insertion;

            create table IF NOT EXISTS laboral_insertion.inscriptions (
                id varchar primary key,
                user_id varchar not null references laboral_insertion.users (id),
                reside boolean default false,
                travel boolean default false,
                checked boolean default false,
                degree varchar not null,
                approved integer default 0,
                average1 real default 0.0,
                average2 real default 0.0,
                work_type varchar not null,
                created timestamptz default now(),
                work_experience boolean default false,
                deleted boolean default false
            );
        """)
    finally:
        cur.close()

@classmethod
def _fromResult(cls, i, r):
    i.id = r['id']
    i.userId = r['user_id']
    i.degree = r['degree']
    i.workType = r['work_type']
    i.reside = r['reside']
    i.travel = r['travel']
    i.checked = r['checked']
    i.workExperience = r['work_experience']
    i.created = r['created']
    i.average1 = r['average1']
    i.average2 = r['average2']
    i.approved = r['approved']
    i.deleted = r['deleted']
    return i

@classmethod
def persist(cls, ctx, inscription):
    ''' un cambio de precondiciones, asi que lo dejo por las dudas '''
    inscription.__dict__['reside'] = False

    ''' crea o actualiza un registro de inscripcion en la base de datos '''
    cur = ctx.con.cursor()
    if not(hasattr(inscription, 'checked')):
        inscription.checked = False
    try:
        if inscription.id is None:
            inscription.id = str(uuid.uuid4())
            ins = inscription.__dict__
            cur.execute('insert into laboral_insertion.inscriptions (id, user_id, degree, work_type, reside, travel, checked, work_experience, average1, average2, approved) values '
                        '(%(id)s, %(userId)s, %(degree)s, %(workType)s, %(reside)s, %(travel)s, %(checked)s, %(workExperience)s, %(average1)s, %(average2)s, %(approved)s )', ins)
        else:
            ins = inscription.__dict__
            cur.execute('update laboral_insertion.inscriptions set user_id = %(userId)s, degree = %(degree)s, work_type = %(workType)s, '
                        'reside = %(reside)s, travel = %(travel)s, checked = %(checked)s, average1 = %(average1)s, average2 = %(average2)s, approved = %(approved)s where id = %(id)s', ins)

    finally:
        cur.close()
