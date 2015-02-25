var app = angular.module('mainApp');


app.controller('LaboralInsertionTermsAndConditionsCtrl',["$scope", "$location", "Session", "LaboralInsertion", function($scope, $location, Session, LaboralInsertion) {


  
  	/**
	 * procesar verificacion de terminos y condiciones
	 */
	$scope.accept = function(){
		
		var session = Session.getCurrentSession(); 
		if((session == null) || (session.selectedUser == null)){
			console.log("error: usuario no seleccionado");
			$location.path('/main');			
		} 
		
		/**
		 * callback en el caso de que el servidor haya devuelto una respuesta correcta
		 * @param ok Booleano que indica si se ha aceptado la condicion
		 */
		callbackOk = function(ok){
			$location.path('/editInsertion');
		}
		
		/**
		 * callback en el caso de que el servidor haya devuelto una respuesta erronea
		 * @param error String con el error
		 */
		callbackError = function(error){
			console.log(error)
			$location.path('/main');
		}

		LaboralInsertion.isTermsAndConditionsAccepted(session.selectedUser, callbackOk, callbackError);
	}



}]);
