var app = angular.module('mainApp');

app.service('Credentials', function($rootScope, Utils, Messages, Session, Config) {

  this.resetPassword = function(username, ok, error) {
    var msg = {
      id: Utils.getId(),
      action: 'resetPassword',
      username: username,
      url: Config.getServerUrl()
    };

    Messages.send(msg,
      function(k) {
        ok(k);
      },
      function(err) {
        error(err);
      });
  }


  this.isLogged = function() {
    var sid = Session.getSessionId();
    if (sid == null) {
      return false;
    }
    var s = Session.getSession(sid);
    if (s == null) {
      return false;
    }
    return ((s.user_id != undefined) && (s.user_id != null));
  }


  this.login = function(creds, ok, error) {
    var msg = {
      "id" : Utils.getId(),
      "user" : creds.username,
      "password" : creds.password,
      "action" : "login"
    }

    Messages.send(msg, function(response) {
      if (response.ok != undefined) {
        ok({user_id:response.user_id, session:response.session});
      } else {
        error(response.error);
      }
    });
  }

  this.logout = function(ok,error) {

    var msg = {
      id: Utils.getId(),
      action: 'logout',
      session: Session.getSessionId()
    };

    Messages.send(msg, function(response) {

      if (response.error != undefined) {
        error(response.error);
      } else {
        ok(response.ok);
      }

    });
  }


  this.changePasswordWithHash = function(creds, hash, ok, error) {
    var msg = {
      id: Utils.getId(),
      action: 'changePassword',
      username: creds.username,
      password: creds.newPassword,
      hash: hash
    };

    Messages.send(msg,
      function(mok) {
        ok(mok);
      },
      function(merror) {
        error(merror);
      });
  }

  this.changePassword = function(creds, ok, error) {

    var sid = Session.getSessionId();
    if ((sid == null) || (sid == '')) {
      error('usuario no autentificado');
      return;
    }

    var msg = {
      id: Utils.getId(),
      action: 'changePassword',
      username: creds.username,
      password: creds.newPassword,
      session: sid
    };

    Messages.send(msg,
      function(mok){
        ok(mok);
      },
      function(merror) {
        error(merror);
      });
  }

})
