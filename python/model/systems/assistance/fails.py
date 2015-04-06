# -*- coding: utf-8 -*-
import inject
import datetime

from model.systems.assistance.date import Date
from model.users.users import Users


class Fails:

    date = inject.attr(Date)
    users = inject.attr(Users)

    def filterUser(self,userId,fails):
        ffails = []
        for f in fails:
            ui = f['userId']
            if userId == ui:
                ffails.append(f)
        return ffails


    def filterFailsToday(self,fails):
        ffails = []
        for f in fails:
            date = f['date']
            if date.replace(hour=0,minute=0,second=0,microsecond=0) == datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0):
                ffails.append(f)
        return ffails


    def toCsv(self,file,users,fails):
        out = open(file,'w')
        try:
            for fail in fails:

                userId = fail['userId']
                user = None
                for u in users:
                    if u['id'] == userId:
                        user = u
                        break


                localDate = self.date.localizeAwareToLocal(self.date.localizeAwareToLocal(fail['date'])).replace(hour=0,minute=0,second=0,microsecond=0)
                f = '{0},{1},{2},{3},{4},{5},{6},{7},{8}'.format(
                    localDate.date(),
                    user['dni'],
                    user['name'],
                    user['lastname'],
                    fail['description'],
                    self.date.localizeAwareToLocal(fail['start']).time() if 'start' in fail else (self.date.localizeAwareToLocal(fail['end']).time() if 'end' in fail else 'no tiene'),
                    self.date.localizeAwareToLocal(fail['startSchedule']).time() if 'startSchedule' in fail else (self.date.localizeAwareToLocal(fail['endSchedule']).time() if 'endSchedule' in fail else 'no tiene'),
                    fail['minutes'] if 'minutes' in fail else '',
                    fail['minutes']-datetime.timedelta(minutes=15) if 'minutes' in fail else '')
                out.write(f)
                out.write('\n')

        finally:
            out.close()
