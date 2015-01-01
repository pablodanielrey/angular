
var app = angular.module('mainApp');

app.factory('Users', function(Messages, Session, Utils) {

  var users = {};

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
