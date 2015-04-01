
var app = angular.module('mainApp');

/**
 * Controlador utilizado para administrar "solicitudes de justificaciones" de una autoridad
 * A grandes rasgos podemos definir dos tipos de solicitudes de justificacion:
 *		Personal: Es la que realiza una persona para si mismo.
 *		Tercera: Es la que realiza una autoridad para un subordinado.
 * El objetivo del controlador es definir solicitudes a un subordinado. Actualmente la autoridad solo puede solicitar "horas extra"
 * El controlador debe identificar el usuario al cual se le va a definir la socicitud, el usuario es definido en otro controlador, se escucha el evento de seleccion de usuario
 */
app.controller('RequestAuthorityCtrl', ["$scope", "$timeout", "$window", "Assistance", "Notifications", "Users", "Session", function($scope, $timeout, $window, Assistance, Notifications, Users, Session) {

	$scope.model = {
		session_user_id: null, //id del usuario de session (correspondiente al jefe que solicita las horas extra)
		user_id: null, //id del usuario para el cual se solicita la justificacion
		id: null, //id de la justificacion solicitada (actualmente solo se pueden solicitar horas extra que equivale a compensatorios)
		startTime: null, //hora de inicio solicitada
		endTime: null, //hora de finalizacion solicitada
		date: null, //actualmente se define un solo dia por solicitud, posteriormente cuando se maneje el calendario se podra definir un rango de dias (para un determinado rango de dias)
		reason: null, //motivo por el cual se solicita las horas extra
		requests: [], //solicitudes de horas extras para el usuario logueado

		//variables correspondientes a la seleccion de usuario
		searchUser: null,
		searchUserPromise: null,
		users: null
	};

	/**
	 * Cargar y chequear session
	 */
	$scope.loadSession = function(){
		if (!Session.isLogged()){
			Notifications.message("Error: Sesion no definida");
			$window.location.href = "/#/logout";
		}
		var session = Session.getCurrentSession();
		$scope.model.session_user_id = session.user_id;
	};

	/**
	 * Obtener solicitudes de horas extra del usuario (jefe)
	 */
	$scope.loadRequests = function(){
		$scope.model.requests = [];
		Assistance.getOvertimeRequests(null, null,
			function callbackOk(requests){
				for(var i = 0; i < requests.length; i++){
					var request = $scope.formatRequest(requests[i]);
					$scope.model.requests.push(request);
				}
			},
			function callbackError(error){
				Notifications.message(error);
				throw new Error(error);
			}
		);
	};

	/**
	 * Dar formato a la solicitud de hora extra
	 */
	$scope.formatRequest = function(request){
		var requestAux = {};
		requestAux.id = request.id;
		requestAux.reason = request.reason;
		requestAux.state = request.state;

		var begin = new Date(request.begin);
		requestAux.date = begin.toLocaleDateString();
		requestAux.startTime = begin.toLocaleTimeString().substring(0, 5);

		var end = new Date(request.end);
		requestAux.endTime = end.toLocaleTimeString().substring(0, 5);

		Users.findUser(request.user_id,
			function findUserCallbackOk(user){
				requestAux.user = user.name + " " + user.lastname;
			},
			function findUserCallbackError(error){
				Notifications.message(error);
				throw new Error(error);
			}
		);
		return requestAux;
	};

	/**
	 * Inicializar
	 */
	$timeout(function() {
		$scope.loadSession();
		$scope.loadRequests();
	},0);




	/******************************************************
	 * METODOS CORRESPONDIENTES A LA SELECCION DE USUARIO *
	 ******************************************************/
	/**
	 * Buscar usuarios
	 */
	$scope.searchUsers = function(){
		$scope.displayListUser = true;
		if($scope.model.searchUserPromise){
			$timeout.cancel($scope.model.searchUserPromise);
		};

		$scope.searchUserPromise = $timeout(
			function(){
				if($scope.search != "") {
					$scope.listUsers();
				}
			}
		,1000);
	};

	$scope.displayListUser = false;

	$scope.isDisplayListUser = function() {
		console.log($scope.displayListUser);
		return $scope.displayListUser;
	}

	/**
 	 * Listar elementos
	 */
	$scope.selectUser = function(user){
		$scope.model.user_id = user.id;
		$scope.model.searchUser = user.name + " " + user.lastname;
		$scope.displayListUser = false;
	};

	/**
 	 * Seleccionar usuario
	 */
	$scope.listUsers = function(){
		Users.listUsers($scope.model.searchUser,
			function(users){
				$scope.model.users = users;
			},
			function(error){
				Notifications.message(error);
			}
		);
	};




	/***********************************************************
	 * METODOS CORRESPONDIENTES AL PROCESAMIENTO DE FORMULARIO *
	 ***********************************************************/

	/**
	 * Dar formato a un timestamp
	 * @param {input type date} date
	 * @param {input type time} time
	 * @returns {Date}
	 */
	$scope.formatTimestamp = function(date, time){
		var timestamp = new Date(date);
		var timeAux = new Date(time);
		timestamp.setHours(timeAux.getHours());
		timestamp.setMinutes(timeAux.getMinutes());
		return timestamp;
	};

	/**
	 * Guardar solicitud en el servidor
	 */
	$scope.persistOvertime = function(){
		var begin = $scope.formatTimestamp($scope.model.date, $scope.model.startTime);
		var end = $scope.formatTimestamp($scope.model.date, $scope.model.endTime);

		var request = {
			date:$scope.model.date,
			begin:begin,
			end:end,
			reason:$scope.model.reason
		};

		Assistance.requestOvertime($scope.model.user_id, request,
			function callbackOk(response){
				$scope.loadRequests();
				Notifications.message("Registro realizado con exito");
			},
			function callbackError(error){
				Notifications.message(error);
			}
		);
	};

	/**
	 * Chequear y guardar solicitud en el servidor
	 */
	$scope.requestOvertime = function(){
		if(($scope.model.date != null) && ($scope.model.startTime != null) && ($scope.model.endTime != null) && ($scope.model.user_id != null)) {
			$scope.persistOvertime();

		} else {
			Notifications.message("Datos incorrectos: Verifique los datos ingresados");
		}
	};

}]);
