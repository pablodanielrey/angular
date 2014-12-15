
/**
 * Controlador para realizar login
 * @param $scope Scope
 * @param WebSocket Servicio de conexion con el WebSocket de login, debe aceptar un usuario y clave, realizar la autenticacion y devolver como respuesta un json con los siguientes datos:
 *		"result":true|false Resultado de la autenticacion
 *		"url": Url de redireccion
 * Supone la existencia de un elemento padre que maneja los eventos dontShowMessage y showMessage para administrar mensajes
 */
app.controller("LoginController", ["$rootScope", "$scope", "$location", "WebSocket", function($rootScope, $scope, $location, WebSocket) {
	$scope.$emit("dontShowMessage");
	var target = null;
	
	/**
	 * autenticar usuario
	 */
	$scope.authenticate = function(url){
		target = url
		if(!$rootScope.socketOpen) {
			$scope.$emit("showMessage", "No es posible realizar la autenticacion");
			return;
		}
		
		var data = {
			"user" : $scope.user,
			"password" : $scope.password,
			"action" : "login"
		}

		WebSocket.send(JSON.stringify(data));
	};
	
	$scope.$on('socketOnOpen', function(event, msg) {
		$rootScope.socketOpen = true;
	});
	
	$scope.$on('socketOnMessage', function(event, msg){
		if(target == null) {
			$scope.$emit("showMessage", "No esta definido el target");
			return
		}

		var response = JSON.parse(msg.data);

		if(response.ok){
			$rootScope.session = response.session
			$location.path(target)
		} else {
			if((response.error == "") || (response.error == null)){
				response.error = "Error no identificado"
			}
		
			$scope.user = "";
			$scope.password = "";
			$scope.$emit("showMessage", response.error);
		}
	});

}]); 
