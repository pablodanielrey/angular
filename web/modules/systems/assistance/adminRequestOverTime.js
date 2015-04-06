
var app = angular.module('mainApp');

app.controller('AdminRequestOverTimeCtrl', ["$scope", "$timeout", "Notifications", "Assistance", "Session", "Users", function($scope, $timeout, Notifications, Assistance, Session, Users) {

	$scope.model = {
		requests : [] //solicitudes de horas extra
	};
	
	/**
	 * Cargar y chequear session
	 */
	$scope.loadSession = function(){
		if (!Session.isLogged()){
			Notifications.message("Error: Sesion no definida");
			$window.location.href = "/#/logout";
		}
	};
	
	/**
	 * Obtener solicitudes de horas extra del usuario
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
	
	$scope.$on('OvertimeUpdatedEvent',function(event, data) {
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
                Notifications.message("El estado fue modificado correctamente");
                $scope.loadRequests();
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
