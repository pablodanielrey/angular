angular
  .module('mainApp')
  .service('Login',Login);

Login.inject = ['$rootScope','$wamp', 'Session'];

function Login($rootScope, $wamp, Session) {

	this.isLogged = function() {
		var sid = Session.getCurrentSession();
		if (sid == null) {
			return false;
		}
		return (sid.user_id != undefined);
	}

  /*
    Chequea que la session actual sea valida
  */
  this.validateSession = function(cok,cerr) {
    var sid = Session.getSessionId();
    if (sid == null) {
      return false;
    }
    $wamp.call('system.session.validate', [sid])
      .then(function(v) {
        cok(v);
      },function(err) {
        cerr(err);
      }
    );
  }

  this.getSessionData = function() {
    return new Promise(function(cok, cerr) {
      var s = Session.getCurrentSession();
      if (s != null) {
        $wamp.call('system.session.validate', [])
        .then(function() {
          cok(s);
        }, function() {
          cerr();
        });
      }
      $wamp.call('', [])
      .then(function() {
        cok();
      }, function() {
        cerr();
      });
    });
  }


	/*
		Loguea al usuario en el servidor y genera tambien la sesion dentro de la cache local
	*/
	this.login = function(username, password) {
    return new Promise(function(cok, cerr) {
  		$wamp.call('system.login', [username,password])
  		.then(function(s) {
  			if (s == null) {
  				cerr('Datos Incorrectos');
  			} else {
          /*
            Creo la sesion dentro de la cache cliente
          */
  				var data = {
  					session_id: s.id,
  					user_id: s.userId,
  					login: {
  						username: s.username,
  						password: password
  					}
  				}
  				Session.create(s.id, data);
  				cok(data);
  			}
  		},function(err) {
  			cerr(err);
  		});
  	});
  }

	this.logout = function() {
    return new Promise(function(cok, cerr) {
      var sid = Session.getSessionId();
  		$wamp.call('system.logout', [sid])
  		.then(function(ok) {
  			if (ok == null) {
  				cerr('');
  			} else {
  				Session.destroy();
  				cok();
  			}
  		},function(err) {
  			cerr(err);
  		});
  	});
  };

};
