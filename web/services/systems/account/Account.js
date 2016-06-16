angular
  .module('mainApp')
  .service('Account', Account);

Account.inject = ['Session', '$wamp']

function Account(Session, $wamp) {

  this.deleteMail = function(uid) {
    return $wamp.call('account.deleteMail', [uid]);
  }

  this.createUser = function(user, student, type) {
    return $wamp.call('account.createUser', [user, student.studentNumber, type.value]);
  }

  this.findByDni = function(dni) {
    return new Promise(function(cok, cerr) {
      var sid = Session.getSessionId();
  		$wamp.call('account.findByDni', [sid, dni])
      .then(function(v) {
        cok(v);
      },function(err) {
        cerr(err);
      });
    });
  }

  this.getTypes = function() {
    return new Promise(function(cok, cerr) {
      var sid = Session.getSessionId();
  		$wamp.call('account.getTypes', [sid])
      .then(function(v) {
        cok(v);
      },function(err) {
        cerr(err);
      });
    });
  }

  this.updateType = function(user, type) {
    return new Promise(function(cok, cerr) {
      var sid = Session.getSessionId();
  		$wamp.call('account.updateType', [sid, user, type])
      .then(function(v) {
        cok(v);
      },function(err) {
        cerr(err);
      });
    });
  }

}
