
/**
 * Controlador para realizar login
 * @param $scope Scope
 * @param WebSocket Servicio de conexion con el WebSocket de login, debe aceptar un usuario y clave, realizar la autenticacion y devolver como respuesta un json con los siguientes datos:
 *		"result":true|false Resultado de la autenticacion
 *		"url": Url de redireccion
 * Supone la existencia de un elemento padre que maneja los eventos dontShowMessage y showMessage para administrar mensajes
 */
app.controller("ListCreateAccountController", ["$rootScope", "$scope", "$location", "WebSocket", function($rootScope, $scope, $location, WebSocket){
	
	if($rootScope.session == null){
		$location.path("login")
	}
	
	if($rootScope.socketOpen){
		var data = {
			"session" : $rootScope.session,
			"action" : "listCreateAccountRequests",
		}
	
		WebSocket.send(JSON.stringify(data));
	} else {
		$scope.$on('socketOnOpen', function(event, msg) {
			var data = {
				"session" : $rootScope.session,
				"action" : "listCreateAccountRequests",
			}
		
			WebSocket.send(JSON.stringify(data));
		});

	}
		
	$scope.$on('socketOnMessage', function(event, msg) {
		var response = JSON.parse(msg.data);

		$scope.users = response.list;
		
	});
}]); 
