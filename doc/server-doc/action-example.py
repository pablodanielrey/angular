# -*- coding: utf-8 -*-


"""
query :
{
  id:,
  action:"",
  session:,
  request:{
      param1:'',
      param2:''
  }

}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor",
  response:{
    [] | params
  }

}
"""

class ActionExample:

    config = inject.attr(Config)
    profiles = inject.attr(Profiles)
    .....


    def handleAction(self, server, message):

        if message['action'] != 'actionName':
            return False

        if 'session' not in message:
            response = {'id':message['id'], 'error':'Parámetros insuficientes'}
            server.sendMessage(response)
            return True

        .....
        ....
        ....

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])
        userId = self.profiles.getLocalUserId(sid)


        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:

            .....
            ....
            ..

            response = {
                'id':message['id'],
                'ok':'',
                'response': ....
            }
            server.sendMessage(response)
            return True


            o en caso de Error

            response = {
                'id':message['id'],
                'error':'error en el servidor'
            }
            server.sendMessage(response)
            return True



        except Exception as e:
            logging.exception(e)
            raise e

        finally:
            con.close()
