
/**
 * Controlador para realizar login
 * @param $scope Scope
 * @param WebSocket Servicio de conexion con el WebSocket de login, debe aceptar un usuario y clave, realizar la autenticacion y devolver como respuesta un json con los siguientes datos:
 *		"result":true|false Resultado de la autenticacion
 *		"url": Url de redireccion
 * Supone la existencia de un elemento padre que maneja los eventos dontShowMessage y showMessage para administrar mensajes
 */
app.controller("LoginController", ["$scope", "$window", "WebSocket", function($scope, $window, WebSocket) {
	var socketOpen = false;
	$scope.$emit("dontShowMessage");

	$scope.authenticate = function(){
		if(!socketOpen) {
			$scope.$emit("showMessage", "No es posible realizar la autenticacion");
			return;
		}
		
		var data = {
			"user" : $scope.user,
			"password" : $scope.password,
		}

		WebSocket.send(JSON.stringify(data));
	};
	
	$scope.$on('socketOnOpen', function(event, msg) { 
		socketOpen = true;
	});
	
	$scope.$on('socketOnMessage', function(event, msg) { 
		var json = JSON.parse(msg.data);
		
		if(json.user == 'ivan'){
			$window.location.href = "http://localhost/angular/index2.html";
		} else {
			var message = "usuario o clave incorrectas"
			$scope.user = "";
			$scope.password = "";
		}
		
		$scope.$emit("showMessage", message);

	});

}]); 
