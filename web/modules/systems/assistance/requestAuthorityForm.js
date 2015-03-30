
var app = angular.module('mainApp');

/**
 * Controlador utilizado para administrar la seleccion del usuario al cual se le quiere asignar horas extra
 */
app.controller('RequestAuthorityFormCtrl', ["$scope", "$timeout", "Assistance", "Notifications", "Users", function($scope, $timeout, Assistance, Notifications, Users) {

	if($scope.model == undefined){
		Notifications.message("Error: Variables del modelo sin definir");
	}
	
	/**
	 * Modificar flag de definicion de solicitud
	 */
	$scope.requestOvertime = function(){
		console.log($scope.model);
		if(($scope.model.date != null) && ($scope.model.startTime != null) && ($scope.model.endTime != null) && ($scope.model.user_id != null)) {
			//TODO Assistance.requestOvertime();
		} else {
			Notifications.message("Datos incorrectos: Verifique los datos ingresados");
		}
	};


}]);
