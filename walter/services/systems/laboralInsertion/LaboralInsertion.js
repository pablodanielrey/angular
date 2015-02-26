
var app = angular.module('mainApp');

app.service('LaboralInsertion', function(Messages, Utils, Session) {

	/**
	 * Aceptar los terminos y condiciones de insercion laboral
	 * @param userId Id de usuario al que se modificaran los terminos y condiciones
	 * @param ok Callback en el caso de que el servidor reciba una respuesta correcta
	 * @param err Callback en el caso de que el servidor reciba una respuesta erronea
	 */
	this.acceptTermsAndConditions = function(userId, ok, err) {
		var msg = {
		  id: Utils.getId(),
		  session: Session.getSessionId(),
		  action:'acceptTermsAndConditions',
		  user_id: userId,
		}

		Messages.send(msg,
			function(response) {
				ok(response);
			},
			function(error) {
				err(error);
			}
		);
	}


	/**
	 * Estan aceptados los terminos y condiciones de insercion laboral?
	 * @param userId Id de usuario al que se modificaran los terminos y condiciones
	 * @param ok Callback en el caso de que el servidor reciba una respuesta correcta
	 * @param err Callback en el caso de que el servidor reciba una respuesta erronea
	 * @response boolean accepted = true | false
	 */
	this.isTermsAndConditionsAccepted = function(userId, ok, err) {
		var msg = {
			id: Utils.getId(),
			session: Session.getSessionId(),
			action:'checkTermsAndConditions',
			user_id: userId,
		}

		Messages.send(msg,
			function(response) {
				ok(response);
			},
			function(error) {
				err(error);
			}
		);
	}


  this.findLaboralInsertionData = function(user_id,ok,err) {
    var msg = {
      id: Utils.getId(),
      session: Session.getSessionId(),
      action:'findLaboralInsertionData',
      laboralInsertion: {
        id: user_id
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

	this.findDegreeData = function(user_id,ok,err) {
		// falta implementar.
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
