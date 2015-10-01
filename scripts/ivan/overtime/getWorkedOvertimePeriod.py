import logging
import sys
import inject
import datetime
sys.path.insert(0,'../../../python')

from model.config import Config
logging.getLogger().setLevel(logging.DEBUG)

from autobahn.asyncio.wamp import ApplicationSession
from asyncio import coroutine


'''
python3 getWorkedOvertimePeriod.py userId date1 date2
python3 getWorkedOvertimePeriod.py e43e5ded-e271-4422-8e85-9f1bc0a61235 "01/01/2015" "31/12/2015"

'''

def config_injector(binder):
    binder.bind(Config,Config('server-config.cfg'))

inject.configure(config_injector)
config = inject.instance(Config)


class WampMain(ApplicationSession):

    def __init__(self,config=None):
        logging.debug('instanciando WampMain')
        ApplicationSession.__init__(self, config)


    @coroutine
    def onJoin(self, details):
        logging.info("********** MINUTOS TRABAJADOS DE REQUERIMIENTOS DE HORAS EXTRAS APROBADAS EN UN PERIODO **********")

        if len(sys.argv) < 4:
            sys.exit("Error de parámetros")

        userId = sys.argv[1]
        
        dateAux = sys.argv[2]
        date1 = datetime.datetime.strptime(dateAux, "%d/%m/%Y").date()

        dateAux = sys.argv[3]
        date2 = datetime.datetime.strptime(dateAux, "%d/%m/%Y").date()
        
        requests = yield from self.call('overtime.getOvertimeRequests', [userId], ["APPROVED"])
        
        seconds = 0
        for request in requests:
            dateAuxStr = request["begin"]
            dateAux = dateAuxStr[:10]
            date = datetime.datetime.strptime(dateAux, "%Y-%m-%d").date()

            if(date >= date1) and (date <= date2):
                seconds += yield from self.call('overtime.getWorkedOvertime', userId, date)

        print(seconds)
            


        #seconds = yield from self.call('overtime.getWorkedOvertime', userId, date)
        
        #logging.info(seconds)

      
if __name__ == '__main__':

        from autobahn.asyncio.wamp import ApplicationRunner
        from autobahn.wamp.serializer import JsonSerializer


        url = config.configs['server_url']
        realm = config.configs['server_realm']
        debug = config.configs['server_debug']

        json = JsonSerializer()
        runner = ApplicationRunner(url=url,realm=realm,debug=debug, debug_wamp=debug, debug_app=debug, serializers=[json])
        runner.run(WampMain)
