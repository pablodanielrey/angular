var app = angular.module('mainApp');

app.factory('Session', function($window) {

	var factory = {};

	factory.sessionIdentifier = 'sessionId';

	factory.getStorage = function() {
		return $window['localStorage'];
	}

	factory.create = function(session, data) {
		s = this.getStorage();
		s.setItem(this.sessionIdentifier,session);
		s.setItem(session,JSON.stringify(data));
	}

	factory.destroy = function(){
		s = this.getStorage();
		var sid = s.getItem(this.sessionIdentifier);
		s.removeItem(sid);
		s.removeItem(this.sessionIdentifier);
	};

	factory.getSessionId = function(){
		s = this.getStorage();
		return s.getItem(this.sessionIdentifier);
	}

	factory.isLogged = function() {
		var sid = this.getSessionId();
		if (sid == null) {
			return false;
		}

		s = this.getStorage();
		json_data = s.getItem(sid);
		if (json_data == null) {
			return false;
		}

		var data = JSON.parse(json_data);
		return (data.user_id != undefined);
	}

	return factory;
});
