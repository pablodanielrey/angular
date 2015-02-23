
var app = angular.module('mainApp');

app.service('Student', function(Messages, Utils, Session) {

  this.findStudentData = function(id,ok,err) {
    var msg = {
      id: Utils.getId(),
      session: Session.getSessionId(),
      action:'findStudentData',
      student: {
        id: id
      }
    }
    Messages.send(msg, function(data) {
      ok(data)
    },
    function(error) {
      err(error);
    })
  }

});
