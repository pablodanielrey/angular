angular
  .module('mainApp')
  .service('Digesto',Digesto);

Digesto.inject = ['$rootScope','$wamp']

function Digesto($rootScope,$wamp) {

  this.createNormative = function(normative,status,visibility,relateds,file,callbackOk,callbackError) {
    $wamp.call('digesto.digesto.createNormative',[normative,status,visibility,relateds,file])
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
}
