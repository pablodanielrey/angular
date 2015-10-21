
angular
  .module('mainApp')
  .service('LaboralInsertion',LaboralInsertion);

LaboralInsertion.inject = ['$rootScope','$wamp','Session']

function LaboralInsertion($rootScope,$wamp,Session) {

  this.find = function(userId, cok, cerr) {
    var sessionId = Session.getSessionId();

    $wamp.call('system.laboralInsertion.find',[userId])
      .then(function(data) {
        cok(data);
      },function(err) {
        cerr(err);
      }
    );
  }


  /**
    obtiene todas las inscripciones de un usuario determinado
  */
  this.findAllByUser = function(userId, cok, cerr) {
    var sessionId = Session.getSessionId();
    $wamp.call('system.laboralInsertion.findAllByUser', [userId])
    .then(function(data) {
      cok(data);
    }, function(err) {
      cerr(err);
    });

  }

}
