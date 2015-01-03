var app = angular.module('mainApp');

app.factory('Session', function(Cache) {

	var factory = {};

	factory.sessionIdentifier = 'sessionId';

	factory.create = function(session, data) {
		Cache.setItem(this.sessionIdentifier,session);
		data.id = session;
		Cache.setItem(session,data);
	}

	factory.destroy = function(){
		var sid = Cache.getItem(this.sessionIdentifier);
		Cache.removeItem(sid);
		Cache.removeItem(this.sessionIdentifier);
	};

	factory.getSessionId = function(){
		return Cache.getItem(this.sessionIdentifier);
	}

  factory.getSession = function(id) {
		return Cache.getItem(id);
	}


	factory.saveSession = function(data) {
		var id = data.id;
		Cache.setItem(id,data);
	}

	factory.isLogged = function() {
		var sid = this.getSessionId();
		if (sid == null) {
			return false;
		}

		var data = Cache.getItem(sid);
		if (data == null) {
			return false;
		}
		return (data.user_id != undefined);
	}

	return factory;
});
