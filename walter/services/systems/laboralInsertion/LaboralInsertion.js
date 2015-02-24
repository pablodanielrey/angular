
var app = angular.module('mainApp');

app.service('LaboralInsertion', function(Messages, Utils, Session) {

  this.findLaboralInsertionData = function(id,ok,err) {
    console.log("LaboralInsertion service -> findLaboralInsertionData")
    var msg = {
      id: Utils.getId(),
      session: Session.getSessionId(),
      action:'findLaboralInsertionData',
      laboralInsertion: {
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
