
var app = angular.module('mainApp');


app.service('Tutors', function(Messages, Utils, Session) {

  this.persistTutorData = function(data,callbackOk,callbackError) {
    var msg = {
      id:Utils.getId(),
      action:'persistTutorData',
      session:Session.getSessionId(),
      request: data
    };

    Messages.send(msg,
      function(data) {
        if (typeof data.error === 'undefined') {
          callbackOk(data.ok);
        } else {
          callbackError(data.error);
        }
      }
    );
  }

});
