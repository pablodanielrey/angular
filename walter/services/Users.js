
var app = angular.module('mainApp');

app.service('Users', function($rootScope, Messages, Session, Utils, Cache, Config) {

  var instance = this;
  this.userPrefix = 'user_';

  $rootScope.$on('UserUpdatedEvent', function(event,id) {
    Cache.removeItem(instance.userPrefix + id);
  });


  this.deleteMail = function(id, callbackOk, callbackError) {
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
  this.confirmMail = function(hash, callbackOk, callbackError) {
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
  this.sendConfirmMail = function(mail_id, callbackOk, callbackError) {
    var msg = {
      id: Utils.getId(),
      session: Session.getSessionId(),
      action: 'confirmMail',
      sub_action: 'generate',
      mail_id: mail_id
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
  this.addMail = function(email, callbackOk, callbackError) {
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
  this.findMails = function(user_id, callbackOk, callbackError) {
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


  this.normalizeUser = function(user) {
    if (user.birthdate != undefined) {
      //user.birthdate = new Date(user.birthdate)
    }
  }



  // obtiene los datos de un usuario cuyo id es el pasado por parámetro.
  this.findUser = function(id, callbackOk, callbackError) {

    // chequeo la cache primero
    var user = Cache.getItem(instance.userPrefix + id);
    if (user != null) {
      callbackOk(user);
      return;
    }

    var msg = {
      id: Utils.getId(),
      session: Session.getSessionId(),
      action: 'findUser',
      user: { id: id }
    }
    Messages.send(msg, function(response) {
      if (response.error != undefined) {
        callbackError(response.error);
      } else {
        var user = response.user;
        instance.normalizeUser(user);
        Cache.setItem(instance.userPrefix + user.id,user);
        callbackOk(user);
      }
    });
  }


  this.updateUser = function(user, callbackOk, callbackError) {

    // elimino ese usuario de la cache
    Cache.removeItem(instance.userPrefix + user.id);

    instance.normalizeUser(user);

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


  this.listUsers = function(search, callbackOk, callbackError) {
    var  msg = {
      id: Utils.getId(),
      action: 'listUsers',
      session: Session.getSessionId(),
      onlyIds: true,
      limit:100,
      search: search,
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
          var user = Cache.getItem(instance.userPrefix + ids[i].id);
          if (user == null) {
            remainingIds.push(ids[i].id);
          } else {
            cachedUsers.push(user);
          }
        }

        // si no hay mas usuarios que pedir. (tengo todos en la cache local)
        if (remainingIds.length <= 0) {
          callbackOk(cachedUsers);
          return;
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
              instance.normalizeUser(user)
              Cache.setItem(instance.userPrefix + user['id'],user);
            }
            callbackOk(cachedUsers.concat(response.users));
          }
        });
      }
    });
  };


});
