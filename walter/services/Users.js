
var app = angular.module('mainApp');

app.factory('Users', function(Messages, Session, Utils, Cache) {

  var users = {};

  users.deleteMail = function(id, callbackOk, callbackError) {
    var msg = {
      id: Utils.getId(),
      session: Session.getSessionId(),
      action: 'removeMail',
      mail_id: id
    }
    Messages.send(msg, function(response) {
      if (response.error != undefined) {
        callbackError(response.error);
      } else {
        callbackOk(response.ok);
      }
    });
  }

  /*
    Dispara la confirmación de un mail dado por el hash
  */
  users.confirmMail = function(hash, callbackOk, callbackError) {
    var msg = {
      id: Utils.getId(),
      session: Session.getSessionId(),
      action: 'confirmMail',
      sub_action: 'confirm',
      hash: hash
    }
    Messages.send(msg, function(response) {
      if (response.error != undefined) {
        callbackError(response.error);
      } else {
        callbackOk(response.ok);
      }
    });
  }

  /*
    Envía un mail de confirmación al email dado por mail_id
  */
  users.sendConfirmMail = function(mail_id, callbackOk, callbackError) {
    var msg = {
      id: Utils.getId(),
      session: Session.getSessionId(),
      action: 'confirmMail',
      sub_action: 'generate',
      mail_id: mail_id,
      url: document.URL
    }
    Messages.send(msg, function(response) {
      if (response.error != undefined) {
        callbackError(response.error);
      } else {
        callbackOk(response.ok);
      }
    });
  }

  /*
    Agrega un email a un usuario.
    formato de email :
    {
      user_id: 'id de usuario',
      email: 'email del usuario'
    }
  */
  users.addMail = function(email, callbackOk, callbackError) {
    var msg = {
      id: Utils.getId(),
      session: Session.getSessionId(),
      action: 'persistMail',
      mail: email
    }
    Messages.send(msg, function(response) {
      if (response.error != undefined) {
        callbackError(error);
      } else {
        callbackOk(response.ok);
      }
    });
  }

  /*
    Encuentra todos los mails de un usuario.
  */
  users.findMails = function(user_id, callbackOk, callbackError) {
    var msg = {
      id: Utils.getId(),
      session: Session.getSessionId(),
      action: 'listMails',
      user_id: user_id
    }
    Messages.send(msg, function(response) {
      if (response.error != undefined) {
        callbackError(error);
      } else {
        callbackOk(response.mails);
      }
    });
  }



  // obtiene los datos de un usuario cuyo id es el pasado por parámetro.
  users.findUser = function(id, callbackOk, callbackError) {
    var msg = {
      id: Utils.getId(),
      session: Session.getSessionId(),
      action: 'findUser',
      user: { id: id}
    }
    Messages.send(msg, function(response) {
      if (response.error != undefined) {
        callbackError(response.error);
      } else {
        callbackOk(response.user);
      }
    });
  }


  users.updateUser = function(user, callbackOk, callbackError) {
    var msg = {
      id: Utils.getId(),
      session: Session.getSessionId(),
      action: 'updateUser',
      user: user
    };
    Messages.send(msg,function(response) {
      if (response.error != undefined) {
        callbackError(response.error);
      } else {
        callbackOk(response.ok);
      }
    });
  }


  users.listUsers = function(callbackOk, callbackError) {
    var  msg = {
      id: Utils.getId(),
      action: 'listUsers',
      session: Session.getSessionId(),
      onlyIds: true
    };
    Messages.send(msg, function(response) {
      if (response.error != undefined) {
        callbackError(response.error);
      } else {

        // tengo los ids de las personas que existen en el server.
        var cachedUsers = [];
        var remainingIds = [];
        var ids = response.users;
        for (var i = 0; i < ids.length; i++) {
          var user = Cache.getItem(ids[i].id);
          if (user == null) {
            remainingIds.push(ids[i].id);
          } else {
            cachedUsers.push(user);
          }
        }

        // hago la llamada al servidor pidiendo los datos de los usuarios de los ids que faltan
        var  msg = {
          id: Utils.getId(),
          action: 'listUsers',
          session: Session.getSessionId(),
          ids: remainingIds
        };
        Messages.send(msg, function(response) {
          if (response.error != undefined) {
            callbackError(response.error);
          } else {
            // actualizo la cache con las personas retornadas.
            for (var i = 0; i < response.users.length; i++) {
              var user = response.users[i];
              Cache.setItem(user['id'],user);
            }
            callbackOk(cachedUsers.concat(response.users));
          }
        });
      }
    });
  };

  return users;

});
