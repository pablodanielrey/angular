
var app = angular.module('mainApp');

app.service('Au24', function(Messages, Utils, Session) {

  this.findAu24ByUserId = function(userId,ok,err) {
    var msg = {
      id: Utils.getId(),
      session: Session.getSessionId(),
      action:'findAu24Data',
      userId: userId,
    }
    
    Messages.send(msg, function(data) {
      ok(data)
    },
    
    function(error) {
      err(error);
    })
  }

});
