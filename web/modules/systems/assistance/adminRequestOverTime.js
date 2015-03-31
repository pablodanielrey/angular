
var app = angular.module('mainApp');

app.controller('AdminRequestOverTimeCtrl', ["$scope", "Notifications", "Assistance" , function($scope, Notifications, Assistance) {

	$scope.model = {
		requests : [] //solicitudes de horas extra
	};
	/*
	  
	/**
	 * Obtener solicitudes de horas extra del usuario
	 *
	$scope.loadRequests = function(){
	
		Assistance.getOvertimeRequestsAdmin(
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
	 *
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
		
		Users.findUser(request.user_id_requestor,
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

		
	$scope.approveRequest = function(request) {
        $scope.updateStatus("APPROVED",request.id);
    };

    $scope.refuseRequest = function(request) {
        $scope.updateStatus("REJECTED",request.id);
    };
	
	$scope.updateStatus = function(status, request_id) {
        Assistance.updateStatusRequestOvertime(request_id, status,
            function(ok) {
                Notifications.message("El estado fue modificado correctamente");
                $scope.loadRequests();
            },
            function(error) {
				Notifications.message(error);
            }
        );
    };
	
	*/

}]);	
