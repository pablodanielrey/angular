var app = angular.module('mainApp');

app.service('Session', function(Cache) {

	this.sessionIdentifier = 'sessionId';

	this.create = function(session, data) {
		Cache.setItem(this.sessionIdentifier,session);
		data.id = session;
		Cache.setItem(session,data);
	}

	this.destroy = function(){
		var sid = Cache.getItem(this.sessionIdentifier);
		Cache.removeItem(sid);
		Cache.removeItem(this.sessionIdentifier);
	};

	this.getSessionId = function(){
		return Cache.getItem(this.sessionIdentifier);
	}

  this.getSession = function(id) {
		return Cache.getItem(id);
	}


	this.saveSession = function(data) {
		var id = data.id;
		Cache.setItem(id,data);
	}

	this.isLogged = function() {
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

});
