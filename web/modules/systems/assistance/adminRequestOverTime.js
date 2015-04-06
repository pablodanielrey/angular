
var app = angular.module('mainApp');

app.controller('AdminRequestOverTimeCtrl', ["$scope", "$timeout", "Notifications", "Assistance", "Session", "Users", function($scope, $timeout, Notifications, Assistance, Session, Users) {

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
		Assistance.getOvertimeRequestsToManage(null,null,
			function callbackOk(requests){
				$scope.model.requests = [];
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


	$scope.loadUser = function(userId){
		var userAux;
		Users.findUser(userId,
			function findUserCallbackOk(user){
				userAux = user;
			},
			function findUserCallbackError(error){
				Notifications.message(error);
				throw new Error(error);
			}
		);
		return userAux;
	}



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

		requestAux.user = $scope.loadUser(request.user_id);

		return requestAux;
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
