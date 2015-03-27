var app = angular.module('mainApp');


app.service('Profiles', function(Utils,Messages) {

  this.checkAccess = function(sessionId, profiles, callbackOk, callbackError) {
    var msg = {
      id: Utils.getId(),
      session: sessionId,
      action: 'checkAccess',
      profiles: profiles
    }
    Messages.send(msg, function(response) {
      if (response.error != undefined) {
        callbackError(response.error);
      } else {
        callbackOk(response.response);
      }
    });
  }

});
