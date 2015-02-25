
var app = angular.module('mainApp');

app.service('LaboralInsertion', function(Messages, Utils, Session) {

  this.acceptTermsAndConditions = function(userId, ok,err) {
    // se aceptan los terminos y condicinoes.
    // y se llama ok();
  }

  this.termsAndConditionsAccepted = function(userId,ok,err) {
    // se consulta si estan aceptadas
    //ok(true);
    //ok(false);
  }

  this.findLaboralInsertionData = function(id,ok,err) {
    var msg = {
      id: Utils.getId(),
      session: Session.getSessionId(),
      action:'findLaboralInsertionData',
      laboralInsertion: {
        id: id
      }
    }
    Messages.send(msg,
      function(data) {
        ok(data);
      },
      function(error) {
        err(error);
      }
    );
  }


  this.updateLaboralInsertionData = function(data, ok, err) {
    var msg = {
      id: Utils.getId(),
      session: Session.getSessionId(),
      action: 'persistLaboralInsertionData',
      laboralInsertion: data
    };

    Messages.send(msg,function(response){
      if (response.error != undefined) {
        callbackError(response.error);
      } else {
        callbackOk(response.ok);
      }
    });
  }

});
