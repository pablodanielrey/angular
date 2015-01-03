var app = angular.module('mainApp');

app.factory('Session', function($window) {

	var factory = {};

	factory.sessionIdentifier = 'sessionId';

	factory.getStorage = function() {
		return $window['localStorage'];
	}

	factory.create = function(session, data) {
		var s = this.getStorage();
		s.setItem(this.sessionIdentifier,session);
		data.id = session;
		s.setItem(session,JSON.stringify(data));
	}

	factory.destroy = function(){
		var s = this.getStorage();
		var sid = s.getItem(this.sessionIdentifier);
		s.removeItem(sid);
		s.removeItem(this.sessionIdentifier);
	};

	factory.getSessionId = function(){
		var s = this.getStorage();
		return s.getItem(this.sessionIdentifier);
	}


  factory.getSession = function(id) {
		var s = this.getStorage();
		var jdata = s.getItem(id);
		if (jdata == null) {
			return null;
		}
		var data = JSON.parse(jdata);
		return data;
	}


	factory.saveSession = function(data) {
		var id = data.id;
		var s = getStorage();
		s.setItem(id,JSON.stringify(s));
	}

	factory.isLogged = function() {
		var sid = this.getSessionId();
		if (sid == null) {
			return false;
		}

		var s = this.getStorage();
		var json_data = s.getItem(sid);
		if (json_data == null) {
			return false;
		}

		var data = JSON.parse(json_data);
		return (data.user_id != undefined);
	}

	return factory;
});
