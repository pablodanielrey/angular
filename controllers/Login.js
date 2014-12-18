
/**
 * Controlador para realizar login
 * @param $scope Scope
 * Supone la existencia de un elemento padre que maneja los eventos dontShowMessage y showMessage para administrar mensajes
 */
app.controller("LoginController", ["$scope", "WebSocket", function($scope, WebSocket){
	
	/**
	 * autenticar usuario
	 */
	$scope.authenticate = function(){
		var data = {
			"user" : $scope.user,
			"password" : $scope.password,
			"action" : "login",
		}
		
		WebSocket.send(JSON.stringify(data));
	};
	
	

}]); 
