
var app = angular.module('mainApp');

app.controller('AdminRequestOverTimeCtrl', ["$scope", "$timeout", "Notifications", "Assistance", "Session", "Users", "Utils", function($scope, $timeout, Notifications, Assistance, Session, Users, Utils) {

	$scope.model = {
		requests : [], //solicitudes de horas extra
		session_user_id : null //id del usuario de session
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
	 * Obtener solicitudes de horas extra del usuario
	 */
	$scope.loadRequests = function() {
		Assistance.getOvertimeRequestsToManage('PENDING',null,
			function callbackOk(requests){
				$scope.model.requests = [];
				for(var i = 0; i < requests.length; i++){
					$scope.formatRequest(requests[i]);
				}
			},
			function callbackError(error){
				Notifications.message(error);
				throw new Error(error);
			}
		);
	};


	$scope.loadUser = function(request){
		Users.findUser(request.user_id,
			function findUserCallbackOk(user){
				request.user = user;
				$scope.model.requests.push(request);
			},
			function findUserCallbackError(error){
				Notifications.message(error);
				throw new Error(error);
			}
		);
	}


	/**
	 * Dar formato a la solicitud de hora extra
	 */
	$scope.formatRequest = function(request){
		var begin = new Date(request.begin);
		request.date = begin.toLocaleDateString();
		request.startTime = Utils.formatTime(begin);

		var end = new Date(request.end);
		request.endTime = Utils.formatTime(end);

		// carga los datos del usuario dentro del request
		$scope.loadUser(request);
	};


	/**
	 * Inicializar
	 */
	$timeout(function() {
		$scope.loadSession();
		$scope.loadRequests();
	},0);

	$scope.$on('OvertimesUpdatedEvent',function(event, data) {
		$scope.loadRequests();
	});

	$scope.$on('OvertimeStatusChangedEvent',function(event, data) {
			$scope.loadRequests();
	});




	/***************************************************************
	 * METODOS CORRESPONDIENTES A LA ADMINISTRACION DE SOLICITUDES *
	 ***************************************************************/
	$scope.updateStatus = function(request_id, status) {
        Assistance.updateRequestOvertimeStatus(request_id, status,
            function(ok) {
							// nada
            },
            function(error) {
							Notifications.message(error);
							throw new Error(error);
            }
        );
    };

	$scope.approveRequest = function(request_id) {
        $scope.updateStatus(request_id, "APPROVED");
    };

    $scope.refuseRequest = function(request_id) {
        $scope.updateStatus(request_id, "REJECTED");
    };

}]);
