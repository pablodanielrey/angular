
app.controller("ListCreateAccountController", ["$scope", "WebSocket", "Session", function($scope, WebSocket, Session){
	
	var data = {
		"session" : Session.getSessionId(),
		"action" : "listCreateAccountRequests",
	}
	
	WebSocket.send(JSON.stringify(data));
	
	/**
	 * Analizar evento onMessage para determinar si es una respuesta a la peticion de la lista de creacion de cuentas
	 */
	$scope.$on('onMessage', function(event, data){
		var response = JSON.parse(data);

		if(response.list != undefined){
			$scope.users = response.list;
		}
	});
}]); 
