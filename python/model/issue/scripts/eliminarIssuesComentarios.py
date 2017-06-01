import logging
import os
from redmine import Redmine

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    r = Redmine(os.environ['REDMINE_URL'], key = os.environ['REDMINE_KEY'], version='3.3', requests={'verify': False})

    trackers = r.tracker.all()
    comentario_tracker = [t for t in trackers if t.name == 'Comentario'][0]

    p = r.project.get('pedidos')

    commentIssues = r.issue.filter(project_id = p.id, subproject_id='*', status_id = '*', tracker_id=comentario_tracker.id)
    for ci in commentIssues:
        logging.info('eliminando : {}'.format(ci.id))
        r.issue.delete(ci.id)
