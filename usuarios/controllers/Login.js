
/**
 * Controlador para realizar login
 * @param $scope Scope
 * Supone la existencia de un elemento padre que maneja los eventos dontShowMessage y showMessage para administrar mensajes
 */
app.controller("LoginController", ["$rootScope", "$scope", "WebSocket", "Session", function($rootScope, $scope, WebSocket, Session){
	
	var ids = new Array();
	
	/**
	 * autenticar usuario
	 */
	$scope.authenticate = function(){
		var id =  (Math.floor((Math.random() * 1000000000) + 1)).toString(); 
		ids[id] = true;
		
		var data = {
			"id" : id,
			"user" : $scope.user,
			"password" : $scope.password,
			"action" : "login",
		}
		
		WebSocket.send(JSON.stringify(data));
	};
	
	/**
	 * Manejo de evento message producido por el socket
 	 * @param event
	 * @param data string JSON: Datos del mensaje
	 */
	$scope.$on('onMessage', function(event, data){

		var response = JSON.parse(data);
		
		if(response.id == undefined)
			return;
		
		if(ids[response.id] == undefined)
			return;
			
		if(response.error != undefined){
			$scope.user = "";
			$scope.password = "";
			var data = {
				"message" : response.error,
			}
			$rootScope.$broadcast("onAppError", JSON.stringify(data));
			return;
		}
		
		if(response.session == undefined){
			$scope.user = "";
			$scope.password = "";
			var data = {
				"message" : "Error de session",
			}
			$rootScope.$broadcast("onAppError", JSON.stringify(data));
			return;
		}
		
		if(response.ok != undefined){
			Session.create(response.session);
			var data = {
				"message" : "Acceso correcto",
			}
			$rootScope.$broadcast("onAppMessage", JSON.stringify(data));
			return;
		}
		
		

	});	
}]); 
