
var app = angular.module('mainApp');

app.factory('Users', function(Messages, Session, Utils) {

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
      session: Session.getSessionId()
    };
    Messages.send(msg, function(response) {
      if (response.error != undefined) {
        callbackError(response.error);
      } else {
        callbackOk(response.users);
      }
    });
  };

  return users;

});
