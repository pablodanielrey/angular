
var app = angular.module('mainApp');

/**
 * Controlador utilizado para administrar "solicitudes de justificaciones" de una autoridad
 * A grandes rasgos podemos definir dos tipos de solicitudes de justificacion:
 *		Personal: Es la que realiza una persona para si mismo.
 *		Tercera: Es la que realiza una autoridad para un subordinado.
 * El objetivo del controlador es definir solicitudes a un subordinado. Actualmente la autoridad solo puede solicitar "horas extra"
 * El controlador debe identificar el usuario al cual se le va a definir la socicitud, el usuario es definido en otro controlador, se escucha el evento de seleccion de usuario
 */
app.controller('RequestAuthorityCtrl', function($scope, $timeout, Assistance, Notifications) {

	$scope.model = {
		user_id: null, //id del usuario para el cual se solicita la justificacion
		id: null, //id de la justificacion solicitada (actualmente solo se pueden solicitar horas extra que equivale a compensatorios)
		time: null, //horas y minutos adicionales solicitados
		date: null, //actualmente se define un solo dia por solicitud, posteriormente cuando se maneje el calendario se podra definir un rango de dias (para un determinado rango de dias)
		request: false //flag para indicar que se ha definido una solicitud
	};
		
	
	/**
	 * Esta definida la solicitud?
	 */
	$scope.isRequest = function(){
		return $scope.model.request;
	};
	
	/**
	 * Modificar flag de definicion de solicitud
	 */
	$scope.changeRequest = function(){
		if((id != null) && (date != null) && (hours != null) && (user_id != null)) {
			request = true;
		} else {
			request = false;
		}
	};
	

	/**
	 * Almacenar solicitud
	 * Para este punto se deben haber chequeado los datos
	 */
	$scope.request = function(){
		var date = $scope.model.date;
		var timeArray = $scope.mode.time.split(":");
		
		date.setHours(timeArray[0]);
		date.setMinutes(timeArray[1]);
					
		var justification = {
			id: $scope.model.id,			
			begin: date,
		}
		
		Assistance.requestLicence(user_id, justification, 
			function(ok){
				Notifications.message("Solicitud cargada con exito");
			},
			function(error){
				Notifications.message(error);
			}
			
		);
	};
	
	/**
	 * Escuchar evento de seleccion de usuario
	 */
	$scope.$on('UserSelectedEvent',function(event, user_id) { 
	    $scope.model.user_id = user_id;
	});
	
});
