
app.controller("CreateAccountController", ["$rootScope", "$scope", "WebSocket", "Session", function($rootScope, $scope, WebSocket, Session){

	var ids = new Array();

	$scope.createAccount = function(){
		var id =  (Math.floor((Math.random() * 1000000000) + 1)).toString(); 
		ids[id] = true;
		
		var data = {
			"id" : id,
			"session" : "",
			"name" : $scope.name,
			"lastname" : $scope.lastname,
			"dni" : $scope.dni,
			"mail" : $scope.mail,
			"reason" : $scope.reason,
			"action" : "createAccountRequest",
		}
		alert(JSON.stringify(data));
		WebSocket.send(JSON.stringify(data));
	}
	
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
			var data = {
				"message" : response.error,
			}
			$rootScope.$broadcast("onAppError", JSON.stringify(data));
		}
		
		if(response.ok != undefined){

			var data = {
				"message" : "Cuenta creada exitosamente",
			}
			$rootScope.$broadcast("onAppMessage", JSON.stringify(data));
			return;
		}


	});	
}]); 
