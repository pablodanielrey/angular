var app = angular.module('mainApp');

app.service('Systems', function($rootScope, Messages, Session, Utils, Cache, Config) {

  this.listSystems = function(callbackOk, callbackError) {
    var  msg = {
      id: Utils.getId(),
      action: 'listSystems',
      session: Session.getSessionId(),
    };
    Messages.send(msg, function(response) {
      if (response.error != undefined) {
        callbackError(response.error);
      } else {
        callbackOk(response.systems);
      }
    });
  }
});
