
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
        ok(data.laboralInsertion);
      },
      function(error) {
        err(error);
      }
    );
  }

  this.updateLaboralInsertionData = function(data, callbackOk, callbackError) {
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

	this.findDegreeData = function(user_id,ok,err) {
		var msg = {
			id:Utils.getId(),
	    action:"listDegrees",
	    session:Session.getSessionId(),
	    user_id:user_id
		}
		Messages.send(msg,
			function(data) {
				ok(data.degrees)
			},
			function(error) {
				err(error)
			}
		);
	}

	/**
	 * Actualizar lenguages
	 * @param user_id Id del usuario al cual se actualizaran las carreras
	 * @param degrees Datos de las carreras
	 * @param ok Callback en el caso de que la actualizacion se realice de forma correcta
 	 * @param error Callback en el caso de que la actualizacion se realice de forma erronea
	 */
	this.updateDegreeData = function(user_id,degrees,ok,err) {
	
		var msg = {
			id:Utils.getId(),
			action:"persistDegreeData",
			session:Session.getSessionId(),
			degrees: degrees,
			user_id:user_id,
		}
		Messages.send(msg,
			function(data) {
				ok(data)
			},
			function(error) {
				err(error)
			}
		);
	}
	

	this.findLanguageData = function(user_id,ok,err) {
		var msg = {
			id:Utils.getId(),
	    action:'listLanguageData',
	    session:Session.getSessionId(),
	    user_id:user_id
		}
		Messages.send(msg,
			function(data) {
				ok(data.languages);
			},
			function(error) {
				err(error);
			}
		);
	}

	/**
	 * Actualizar lenguages
	 * @param user_id Id del usuario al cual se actualizaran los lenguajes
	 * @param languages Datos de los lenguajes
	 * @param ok Callback en el caso de que la actualizacion se realice de forma correcta
 	 * @param error Callback en el caso de que la actualizacion se realice de forma erronea
	 */
	this.updateLanguageData = function(user_id, languages,ok,err) {
		var msg = {
			id:Utils.getId(),
			action:'persistLanguage',
			session:Session.getSessionId(),
			user_id:user_id,
			languages:languages,
		}
		
		Messages.send(msg,
			function(data) {
				ok(data)
			},
			function(error) {
				err(error)
			}
		);
	}

});
