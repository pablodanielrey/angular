
/**
 * Controlador para realizar login
 * @param $scope Scope
 * @param WebSocket Servicio de conexion con el WebSocket de login, debe aceptar un usuario y clave, realizar la autenticacion y devolver como respuesta un json con los siguientes datos:
 *		"result":true|false Resultado de la autenticacion
 *		"url": Url de redireccion
 * Supone la existencia de un elemento padre que maneja los eventos dontShowMessage y showMessage para administrar mensajes
 */
app.controller("CreateAccountController", ["$scope", "WebSocket", function($scope, WebSocket){

	$scope.createAccount = function(){
		var data = {
			"name" : $scope.name,
			"lastname" : $scope.lastname,
			"dni" : $scope.dni,
			"mail" : $scope.mail,
			"action" : "createAccountRequest",
		}
		
		WebSocket.send(JSON.stringify(data));
	}
}]); 
