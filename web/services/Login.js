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
		return (data.user_id != undefined);
	}

	/*
		Loguea al usuario en el servidor y genera tambien la sesion dentro de la cache local
	*/
	this.login = function(username, password, cok, cerr) {
		$wamp.call('system.login', [username,password])
		.then(function(s) {

			if (sid == null) {
				cerr('');

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
		}),function(err) {
			cerr(err);
		};
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
		}),function(err) {
			cerr(err);
		};
	}

});
