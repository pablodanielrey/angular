
var app = angular.module('mainApp');

/**
 * Controlador utilizado para administrar la seleccion del usuario al cual se le quiere asignar horas extra
 */
app.controller('RequestAuthorityShowRequestsCtrl', ["$scope", "Notifications", function($scope, Notifications) {

	if($scope.model == undefined){
		Notifications.message("Error: Variables del modelo sin definir");
	}


}]);
