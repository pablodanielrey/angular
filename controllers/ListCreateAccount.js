
app.controller("ListCreateAccountController", ["$scope", "WebSocket", "Session", "uuid4", function($scope, WebSocket, Session, uuid4){
	
	var ids = new Array();
	var id = uuid4.generate();
	ids[id] = "listCreateAccountRequests";
	
	var data = {
		"id" : id,
		"session" : Session.getSessionId(),
		"action" : "listCreateAccountRequests",
	}
	
	WebSocket.send(JSON.stringify(data));
	
	/**
	 * Analizar evento onMessage para determinar si es una respuesta a la peticion de la lista de creacion de cuentas
	 */
	$scope.$on('onMessage', function(event, data){

		var response = JSON.parse(data);
		
		if(response.id == undefined){
			return;
		
		}
		if(ids[response.id] == undefined){
			return;
		}
			
		if(response.error != undefined){
			var data = {
				"message" : response.error,
			}
			$rootScope.$broadcast("onAppError", JSON.stringify(data));
		}

		if(response.ok != undefined){
			$scope.users = response.list;
		}
			
	});
}]); 
