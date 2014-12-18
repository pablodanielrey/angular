
/**
 * Controlador para administrar usuario
 * @param $scope Scope
 * @param WebSocket Servicio de conexion con el WebSocket de login, debe aceptar un usuario y clave, realizar la autenticacion y devolver como respuesta un json con los siguientes datos:
 *		"result":true|false Resultado de la autenticacion
 *		"url": Url de redireccion
 * Supone la existencia de un elemento padre que maneja los eventos dontShowMessage y showMessage para administrar mensajes
 */
app.controller("AdminUserController", ["$scope", "$cookies", "WebSocket", function($scope, $cookies, WebSocket){

	//Al acceder al controlador se deben obtener los datos de usuario del servidor
	var data = {
		"action" : "getUserSession",
		"session" : $cookies.fceSession,
	}
		
	WebSocket.send(JSON.stringify(data));
		
	/**
	 * Analizar evento onMessage para determinar si es una respuesta a la peticion de los datos de usuario del servidor
	 */
	$scope.$on('onMessage', function(event, data){
		var response = JSON.parse(data);

		if((response.name != undefined)
		&& (response.lastname != undefined)
		&& (response.dni != undefined)
		&& (response.mail != undefined)){
			$scope.name =  response.name
			$scope.lastname =  response.lastname
			$scope.mail =  response.mail
			$scope.dni =  response.dni
		}
	});


	/**
	 * Modificar datos de usuario de la session
	 */
	$scope.modify = function(){
		var data = {
			"session" : $cookies.fceSession,
			"name" : $scope.name,
			"lastname" : $scope.lastname,
			"dni" : $scope.dni,
			"mail" : $scope.mail,
			"action" : "modifyUserSession",
		}
		
		WebSocket.send(JSON.stringify(data));
	}
	
}]); 
