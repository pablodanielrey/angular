angular
	.module('mainApp')
	.service('Systems',Systems);

Systems.inject = ['Utils','Session','$wamp'];

function Systems (Utils, Session, $wamp) {

  this.listSystems = function() {
    return new Promise(function(cok, cerr) {
      var sid = Session.getSessionId();
  		$wamp.call('fce.listSystems', [sid])
      .then(function(v) {
        cok(v);
      },function(err) {
        cerr(err);
      });
    });
  }

  this.changePassword = function(password) {
    return new Promise(function(cok, cerr) {
      var sid = Session.getSessionId();
  		$wamp.call('fce.changePassword', [sid, password])
      .then(function(v) {
        cok(v);
      },function(err) {
        cerr(err);
      });
    });
  }

}
