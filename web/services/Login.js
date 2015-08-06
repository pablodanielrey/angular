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

	this.login = function(username, password, cok, cerr) {
		$wamp.call('system.login', [username,password])
		.then(function(sid) {
			if (sid == null) {
				cerr('');
			} else {
				cok(sid);
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
				cok();
			}
		}),function(err) {
			cerr(err);
		};
	}

});
