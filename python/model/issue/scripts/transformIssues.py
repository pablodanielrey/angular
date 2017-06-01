import logging
import os
from redmine import Redmine

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    r = Redmine(os.environ['REDMINE_URL'], key = os.environ['REDMINE_KEY'], version='3.3', requests={'verify': False})
    #for p in r.project.all():
    #    logging.info('{} {}'.format(p.identifier, p.name))

    trackers = r.tracker.all()
    tareas_tracker = [t for t in trackers if t.name == 'Tareas'][0]
    errores_tracker = [t for t in trackers if t.name == 'Errores'][0]

    p = r.project.get('pedidos')
    """ cambio todos los pedidos a Tareas como quedamos """
    for i in r.issue.filter(project_id=p.id, subproject_id='*', status_id='*', tracker_id=errores_tracker.id):
        if (i.tracker.name == 'Errores'):
            logging.info('Cambiando tracker a {} - {}'.format(i.id, i.subject))
            i.tracker_id = tareas_tracker.id
            i.save()

    """ para probar la metodología usando un solo pedidos """
    """ transformar los subtareas en entradas en el journal """
    parentIssues = r.issue.filter(issue_id = 2623, status_id = '*')
    hijosABorrar = []
    for parentIssue in parentIssues:
        logging.info('Buscando hijos de : {} {}'.format(parentIssue.id, parentIssue.subject))
        #hijos = sorted([i for i in r.issue.filter(parent_issue_id = parentIssue.id)], key=lambda x: x.id)
        hijos = sorted([i for i in parentIssue.children], key=lambda x: x.id)
        for hijo in hijos:
            i = r.issue.filter(issue_id = hijo.id, status_id = '*')[0]
            hijosABorrar.append(i.id)

            """
                respuesta de ejemplo de un issue hijo
                {"issues":[{"id":2624,"project":{"id":3,"name":"Soporte"},"tracker":{"id":4,"name":"Comentario"},"status":{"id":1,"name":"Nueva"},"priority":{"id":2,"name":"Normal"},"author":{"id":14,"name":"Maximiliano Saucedo"},"parent":{"id":2623},"subject":"Instalar Windows 7","description":"Deje subiendo los archivos al google drive, en el pendrive rojo dejo listo windows 7.","start_date":"2017-04-26","done_ratio":0,"custom_fields":[{"id":1,"name":"creador","value":""},{"id":2,"name":"from","value":""},{"id":3,"name":"uuid","value":""}],"created_on":"2017-04-26T22:34:45Z","updated_on":"2017-04-26T22:34:45Z"}],"total_count":1,"offset":0,"limit":100}

                me importan los datos :
                author
                created_on
                description
            """

            logging.info(i)
            author_id = i.author.id
            author = r.user.get(author_id).login
            created_on = i.created_on
            description = i.description
            logging.info('Parent {} - pid {} fecha {} autor {} Nota {}'.format(parentIssue.id, i.id, created_on, author, description))

            r2 = Redmine(os.environ['REDMINE_URL'], key = os.environ['REDMINE_KEY'], version='3.3', requests={'verify': False}, impersonate=author)
            pi = r2.issue.update(parentIssue.id, private_note=False, notes=description, updated_on=created_on.date())
