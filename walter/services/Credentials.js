var app = angular.module('mainApp');

app.service('Credentials', ['$rootScope','Utils','Messages','Session','Config',

  function($rootScope, Utils, Messages, Session, Config) {

    /*
    info local del explorador para detectar errores
    */
    this.getLocalInfo = function() {
      var info = {
        'appCodeName': navigator.appCodeName,
        'appName': navigator.appName,
        'appVersion': navigator.appVersion,
        'cookieEnabled': navigator.cookieEnabled,
        'language': navigator.language,
        'onLine': navigator.onLine,
        'platform': navigator.platform,
        'product': navigator.product,
        'userAgent': navigator.userAgent
      };
      return info;
    }


    this.resetPassword = function(username, ok, error) {
      var info = JSON.stringify(this.getLocalInfo());

      var msg = {
        id: Utils.getId(),
        action: 'resetPassword',
        username: username,
        info: info
      };

      Messages.send(msg, function(response) {
        if (response.error != undefined) {
          error(response.error);
        } else {
          ok(response.ok);
        }
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
      var info = JSON.stringify(this.getLocalInfo());

      var msg = {
        "id" : Utils.getId(),
        "user" : creds.username,
        "password" : creds.password,
        "action" : "login",
        "info": info
      };

      Messages.send(msg, function(response) {
        if (response.ok != undefined) {
          ok({user_id:response.user_id, session:response.session});
        } else {
          error(response.error);
        }
      });
    }

    this.logout = function(ok,error) {
      var info = JSON.stringify(this.getLocalInfo());

      var msg = {
        id: Utils.getId(),
        action: 'logout',
        session: Session.getSessionId(),
        info: info
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
      var info = JSON.stringify(this.getLocalInfo());

      var msg = {
        id: Utils.getId(),
        action: 'changePassword',
        username: creds.username,
        password: creds.newPassword,
        hash: hash,
        info: info
      };

      Messages.send(msg, function(response) {
        if (response.error != undefined) {
          error(response.error);
        } else {
          ok(response.ok);
        }
      });
    }

    this.changePassword = function(creds, ok, error) {

      var sid = Session.getSessionId();
      if ((sid == null) || (sid == '')) {
        error('usuario no autentificado');
        return;
      }

      var info = JSON.stringify(this.getLocalInfo());

      var msg = {
        id: Utils.getId(),
        action: 'changePassword',
        username: creds.username,
        password: creds.newPassword,
        session: sid,
        info: info
      };

      Messages.send(msg, function(response) {
        if (response.error != undefined) {
          error(response.error);
        } else {
          ok(response.ok);
        }
      });
    }

}])
