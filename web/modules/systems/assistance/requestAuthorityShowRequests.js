
var app = angular.module('mainApp');

/**
 * Controlador utilizado para administrar la seleccion del usuario al cual se le quiere asignar horas extra
 */
app.controller('RequestAuthorityShowRequestsCtrl', ["$scope", "$timeout", "Assistance", "Notifications", "Users", function($scope, $timeout, Assistance, Notifications, Users) {

	if($scope.model == undefined){
		Notifications.message("Error: Variables del modelo sin definir");
	}
	
	
	
	


}]);
