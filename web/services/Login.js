angular
  .module('mainApp')
  .service('Login',Login);

Login.inject = ['$rootScope','$wamp', 'Session'];

function Login($rootScope, $wamp, Session) {

	this.isLogged = function() {
    return new Promise(function(cok, cerr) {
      var sid = Session.getCurrentSession();
  		if (sid == null) {
  			cok(false);
  		} else {
  		  cok(sid.user_id != undefined);
      }
    });
	}

  this.validateSession = function() {
    return new Promise(function(cok, cerr) {
      var sid = Session.getSessionId();
      if (sid == null) {
        cok(false);
      } else {
        $wamp.call('system.session.validate', [sid])
          .then(function(v) {
            cok(v);
          },function(err) {
            cerr(err);
          }
        );
      }
    });
  }

  this.getSessionData = function() {
    return new Promise(function(cok, cerr) {
      var s = Session.getCurrentSession();
      if (s != null) {
        $wamp.call('system.session.validate', [])
        .then(function() {
          cok(s);
        }, function() {
          cerr(Error());
        });
      }
    });
  }


	/*
		Loguea al usuario en el servidor y genera tambien la sesion dentro de la cache local
	*/
	this.login = function(username, password) {
    return new Promise(function(cok, cerr) {
      $wamp.call('system.login', [username, password])
  		.then(function(s) {
  			if (s == null) {
  				cerr(Error('Datos Incorrectos'));
  			} else {
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
  				cerr(Error('resultado = null'));
  			} else {
  				Session.destroy();
  				cok();
  			}
  		},function(err) {
  			cerr(err);
  		});
    });
  };

  this.testUser = function(username) {
    return $wamp.call('system.testUser', [username])
  }

  this.hasOneRole = function(roles) {
    return new Promise(function(cok, cerr) {
      var sid = Session.getSessionId();
  		$wamp.call('system.profile.hasOneRole', [sid, roles])
      .then(function(v) {
        cok(v);
      },function(err) {
        cerr(err);
      });
    });
  };

};
