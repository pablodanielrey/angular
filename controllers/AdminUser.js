
/**
 * Controlador para administrar usuario
 * @param $scope Scope
 * @param WebSocket Servicio de conexion con el WebSocket de login, debe aceptar un usuario y clave, realizar la autenticacion y devolver como respuesta un json con los siguientes datos:
 *		"result":true|false Resultado de la autenticacion
 *		"url": Url de redireccion
 * Supone la existencia de un elemento padre que maneja los eventos dontShowMessage y showMessage para administrar mensajes
 */
app.controller("AdminUserController", ["$scope", function($scope){
	
	var data = {
		"action" : "getUserSession",
	}
		
	$scope.$emit("onEvent", JSON.stringify(data));
			
	$scope.$on('userData', function(event, data){
		var response = JSON.parse(data);

		$scope.name =  response.name
		$scope.lastname =  response.lastname
		$scope.mail =  response.mail
		$scope.dni =  response.dni
	
	});

	

	
}]); 
