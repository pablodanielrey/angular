
var app = angular.module('mainApp');

/**
 * Controlador utilizado para administrar la seleccion del usuario al cual se le quiere asignar horas extra
 */
app.controller('RequestAuthorityFormCtrl', ["$scope", "$timeout", "Assistance", "Notifications", "Users", function($scope, $timeout, Assistance, Notifications, Users) {

	if($scope.model == undefined){
		Notifications.message("Error: Variables del modelo sin definir");
	}
	
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
