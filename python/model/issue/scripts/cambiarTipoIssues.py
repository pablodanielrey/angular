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
