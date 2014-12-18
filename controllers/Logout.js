
/**
 * Controlador para realizar login
 * @param $scope Scope
 * Supone la existencia de un elemento padre que maneja los eventos dontShowMessage y showMessage para administrar mensajes
 */
app.controller("LogoutController", ["$scope", "Session",  function($scope, Session){

	Session.destroy();
	Session.goHome();
	
}]); 
