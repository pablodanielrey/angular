
var app = angular.module('mainApp');

/**
 * Controlador utilizado para administrar "solicitudes de justificaciones" de una autoridad
 * A grandes rasgos podemos definir dos tipos de solicitudes de justificacion:
 *		Personal: Es la que realiza una persona para si mismo.
 *		Tercera: Es la que realiza una autoridad para un subordinado.
 * El objetivo del controlador es definir solicitudes a un subordinado. Actualmente la autoridad solo puede solicitar "horas extra"
 * El controlador debe identificar el usuario al cual se le va a definir la socicitud, el usuario es definido en otro controlador, se escucha el evento de seleccion de usuario
 */
app.controller('RequestAuthorityCtrl', ["$scope", "$timeout", "$window", "Assistance", "Notifications", "Session", function($scope, $timeout, $window, Assistance, Notifications, Session) {

	$scope.model = {
		user_id: null, //id del usuario para el cual se solicita la justificacion
		id: null, //id de la justificacion solicitada (actualmente solo se pueden solicitar horas extra que equivale a compensatorios)
		startTime: null, //hora de inicio solicitada
		endTime: null, //hora de finalizacion solicitada
		date: null, //actualmente se define un solo dia por solicitud, posteriormente cuando se maneje el calendario se podra definir un rango de dias (para un determinado rango de dias)
		reason: null, //motivo por el cual se solicita las horas extra
		requests: [] //solicitudes de horas extras para el usuario logueado
	};
	
	
	
	$scope.loadRequests = function(){
	
		var session = Session.getCurrentSession(); //obtengo sesión actual
		if(session == null) {
			Notifications.message("Error: Sesion no definida");
			$window.location.href = "/#/logout"; 
		}
		else if(session.user_id == null){
			Notifications.message("Error: Usuario de sesion no definido");
			$window.location.href = "/#/logout";
		} else {
			
			$scope.model.requests [
				{
					userName:"Juan", 
					date:null,
					startTime:null,
					endTime:null,
					reason:null,
					status:null
				},
				{
					userName:"Juan", 
					date:null,
					startTime:null,
					endTime:null,
					reason:null,
					status:null
				}
			]
		
			/** TODO 
			Assistance.getOvertimeRequests(s.user_id,
				function callbackOk(requests){
					var request = {}
					for(var i = 0; i < requests.length; i++){
						request.id = requests[i].id;
						User.findUser(requests[i].user_id,
							function findUserCallbackOk(user){
								request.user = user;
							},
							function findUserCallbackError(error){
								Notifications.message(error);
								throw new Error(error);
							}
						);
					}
					$scope.model.requests.push(request);
				},
				function callbackError(error){
					Notifications.message(error);
					throw new Error(error);
				}
			); */
		}
	}
	
	
	$timeout(function() { 
		$scope.loadRequests();
	},0);
		

	
}]);
