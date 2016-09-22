import logging
import sys
import inject
import datetime
sys.path.insert(0,'../../../python')

from model.config import Config
logging.getLogger().setLevel(logging.INFO)

from autobahn.asyncio.wamp import ApplicationSession
from asyncio import coroutine


'''
python3 getWorkedOvertimePeriod.py date1 date2 
python3 getWorkedOvertimePeriod.py "01/01/2015" "31/12/2015"

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
        print("********** MINUTOS TRABAJADOS DE REQUERIMIENTOS DE HORAS EXTRAS APROBADAS EN UN PERIODO **********")

        if len(sys.argv) < 3:
            sys.exit("Error de parámetros")
        
        dateAux = sys.argv[1]
        date1 = datetime.datetime.strptime(dateAux, "%d/%m/%Y").date()

        dateAux = sys.argv[2]
        date2 = datetime.datetime.strptime(dateAux, "%d/%m/%Y").date()
        
        requests = yield from self.call('overtime.getOvertimeRequests', [], ["APPROVED"])
        
        usersId = []
        
        for request in requests:
            if request["user_id"] not in usersId:
                usersId.append(request["user_id"])
        
        users = yield from self.call('users.findUsersByIds', usersId)       


        toPrint = []
        for user in users:
            requests = yield from self.call('overtime.getOvertimeRequests', [user["id"]], ["APPROVED"])
            
            seconds = 0
            if len(requests) == 0:
                continue;
                
            for request in requests:
                dateAuxStr = request["begin"]
                dateAux = dateAuxStr[:10]
                date = datetime.datetime.strptime(dateAux, "%Y-%m-%d").date()

                if(date >= date1) and (date <= date2):
                    seconds += yield from self.call('overtime.getWorkedOvertime', user["id"], date)

            if seconds > 0:
                append = user["id"] + ", " + user["name"] + ", " + user["lastname"] + ", " + user["dni"] + ", " + str(round(seconds/3600))
                toPrint.append(append)
        

        for pr in toPrint:
            print(pr)
    
        sys.exit()
      
if __name__ == '__main__':

        from autobahn.asyncio.wamp import ApplicationRunner
        from autobahn.wamp.serializer import JsonSerializer


        url = config.configs['server_url']
        realm = config.configs['server_realm']
        debug = config.configs['server_debug']

        json = JsonSerializer()
        runner = ApplicationRunner(url=url,realm=realm,debug=debug, debug_wamp=debug, debug_app=debug, serializers=[json])
        runner.run(WampMain)
