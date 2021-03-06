angular
  .module('mainApp')
  .service('Digesto',Digesto);

Digesto.inject = ['$rootScope','$wamp','Session']

function Digesto($rootScope,$wamp,Session) {

  this.createNormative = function(normative,callbackOk,callbackError) {
    sessionId = Session.getSessionId();
    $wamp.call('digesto.digesto.createNormative',[sessionId,normative,normative.status.value,normative.visibility,normative.relateds,normative.file])
    .then(function(normativeId) {
      if (normativeId != null) {
        callbackOk(normativeId);
      } else {
        callbackError('Error')
      }
    }),function(err) {
      callbackError('Error!!!');
    };
  };


  this.loadIssuers = function(type,callbackOk,callbackError) {
    $wamp.call('digesto.digesto.loadIssuers',[type])
    .then(function(issuers) {
      if (issuers != null) {
        callbackOk(issuers);
      } else {
        callbackError('Error');
      }
    }),function(error) {
      callbackError('Error')
    };
  };

  this.findNormative = function(text,filters,callbackOk,callbackError) {
    $wamp.call('digesto.digesto.findNormative',[text,filters])
    .then(function(normatives) {
      if (normatives != null) {
        callbackOk(normatives);
      } else {
        callbackError('Error');
      }
    }),function(error) {
      callbackError('Error');
    };
  };

  this.findNormativeById = function(id,callbackOk,callbackError) {
    $wamp.call('digesto.digesto.findNormativeById',[id])
    .then(function(normatives) {
      if (normatives != null) {
        callbackOk(normatives);
      } else {
        callbackError('Error');
      }
    }),function(error) {
      callbackError('Error');
    };
  };
}
