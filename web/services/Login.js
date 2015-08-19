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

  this.getUserId = function() {
    var s = Session.getCurrentSession();
    return s.user_id;
  }


	/*
		Loguea al usuario en el servidor y genera tambien la sesion dentro de la cache local
	*/
	this.login = function(username, password, cok, cerr) {
		$wamp.call('system.login', [username,password])
		.then(function(s) {
			if (s == null) {
				cerr('Datos Incorrectos');
			} else {
        /*
          Creo la sesion dentro de la cache cliente
        */
				var data = {
					session_id: s.session_id,
					user_id: s.user_id,
					login: {
						username: username,
						password: password
					}
				}
				Session.create(s.session_id, data);
				cok(s.session_id);
			}
		},function(err) {
			cerr(err);
		});
	}

	this.logout = function(sid, cok, cerr) {
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
	}

};
