angular
	.module('mainApp')
	.service('Assistance',Assistance);

Assistance.inject = ['Utils','Session','$wamp'];

function Assistance (Utils, Session, $wamp) {

	this.getAssistanceData = function (userIds, start, end) {
		return $wamp.call('assistance.getAssistanceData',[userIds, start, end]);
	}

	this.getJustifications = function (userId, start, end, isAll) {
		return $wamp.call('assistance.getJustifications',[userId, start, end, isAll]);
	}

	this.createSingleDateJustification = function(date, userId, justClazz, justModule) {
		return new Promise(function(cok, cerr) {
      var sid = Session.getSessionId();
  		$wamp.call('assistance.createSingleDateJustification', [sid, date, userId, justClazz, justModule])
      .then(function(v) {
        cok(v);
      },function(err) {
        cerr(err);
      });
    });
	}

};
