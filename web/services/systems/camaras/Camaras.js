angular
  .module('mainApp')
  .service('Camaras',Camaras);

Camaras.inject = ['$rootScope','$wamp','Session'];

function Camaras($rootScope,$wamp,Session) {

  this.findAllCamaras = findAllCamaras;
  this.findRecordings = findRecordings;

  function findAllCamaras(callbackOk,callbackError) {
    sessionId = Session.getSessionId();
    $wamp.call('camaras.camaras.findAllCameras', [])
    .then(function(res) {
      if (res != null) {
        callbackOk(res);
      } else {
        callbackError('Error');
      }
    },function(err) {
      callbackError('Error');
    });
  }

  function findRecordings(start,end,camaras,callbackOk,callbackError) {
    sessionId = Session.getSessionId();
    $wamp.call('camaras.camaras.findRecordings', [start,end,camaras])
    .then(function(res) {
      if (res != null) {
        callbackOk(res);
      } else {
        callbackError('Error');
      }
    },function(err) {
      callbackError('Error');
    });
  }
}
