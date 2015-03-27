
var app = angular.module('mainApp');


app.service('Tutors', function(Messages, Utils, Session) {

  this.persistTutorData = function(data,ok,err) {
    var msg = {
      id:Utils.getId(),
      action:'persistTutorData',
      session:Session.getSessionId(),
      request: data
    };

    Messages.send(msg,
      function(data) {
        ok(data.ok);
      },
      function(error) {
        err(data.error);
      }
    );
  }

});
