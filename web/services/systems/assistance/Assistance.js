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

	this.getJustificationData = function (userId, date, justClazz, justModule) {
		return $wamp.call('assistance.getJustificationData',[userId, date, justClazz, justModule]);
	}

	this.getScheduleData = function (userIds, start, end) {
		return $wamp.call('assistance.getScheduleData',[userIds, start, end]);
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

	this.createRangedTimeWithReturnJustification = function(start, end, userId, justClazz, justModule) {
		return new Promise(function(cok, cerr) {
      var sid = Session.getSessionId();
  		$wamp.call('assistance.createRangedTimeWithReturnJustification', [sid, start, end, userId, justClazz, justModule])
      .then(function(v) {
        cok(v);
      },function(err) {
        cerr(err);
      });
    });
	}

	this.createRangedJustification = function(start, days, userId, justClazz, justModule) {
		return new Promise(function(cok, cerr) {
      var sid = Session.getSessionId();
  		$wamp.call('assistance.createRangedJustification', [sid, start, days, userId, justClazz, justModule])
      .then(function(v) {
        cok(v);
      },function(err) {
        cerr(err);
      });
    });
	}

	this.createRangedTimeWithoutReturnJustification = function(start, userId, justClazz, justModule) {
		return new Promise(function(cok, cerr) {
      var sid = Session.getSessionId();
  		$wamp.call('assistance.createRangedTimeWithoutReturnJustification', [sid, start, userId, justClazz, justModule])
      .then(function(v) {
        cok(v);
      },function(err) {
        cerr(err);
      });
    });
	}

	this.changeStatus = function(justification, status) {
		return new Promise(function(cok, cerr) {
      var sid = Session.getSessionId();
  		$wamp.call('assistance.changeStatus', [sid, justification, status])
      .then(function(v) {
        cok(v);
      },function(err) {
        cerr(err);
      });
    });
	}

};
