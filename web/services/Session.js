var app = angular.module('mainApp');

app.service('Session', function(Cache) {

	this.sessionIdentifier = 'sessionId';

	this.create = function(session, data) {
		Cache.setItem(this.sessionIdentifier,session);
		data.sessionId = session;
		Cache.setItem(session,data);
	}

	this.destroy = function() {
		var sid = Cache.getItem(this.sessionIdentifier);
		Cache.removeItem(sid);
		Cache.removeItem(this.sessionIdentifier);
	};

	this.getSessionId = function() {
		return Cache.getItem(this.sessionIdentifier);
	}

  this.getSession = function(id) {
		return Cache.getItem(id);
	}

	this.getCurrentSession = function() {
		var sid = this.getSessionId();
		if (sid == null) {
			return null;
		}
		var data = Cache.getItem(sid);
		return data;
	}

  /**
   * Obtener id de usuario de sesion
   */
  this.getCurrentSessionUserId = function(){
    var session = this.getCurrentSession();
    return session.user_id;
  };

	this.saveSession = function(data) {
		var id = data.sessionId;
		Cache.setItem(id,data);
	}


});
