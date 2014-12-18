
app.controller("MainAdminController", ["$rootScope", "$scope", "$location", "WebSocket", "Session", function($rootScope, $scope, $location, WebSocket, Session) {
	$rootScope.socketOpen = false;
	$location.path("/loading");
	
	/**
	 * Crear session
	 * @param response JSON con el mensaje recibido
	 */
	var getActionFromMessage = function(message){

		//si esta definida la accion en el mensaje, se retorna
		if(message.action != undefined){
			return message.action;
		}
		
		//si no esta definida la accion en el mensaje se determinara en funcion de los parametros recibidos
		if(message.session != undefined){
			return "createSession";
		}
		
		if(message.ok != undefined){
			if(message.ok.substring(0, 23) == "request created with id"){
				return "accountCreated";
			}
		}
	};
	
	/**
	 * Manejo de evento apertura de socket
	 * @param data string JSON: Datos del mensaje 
	 */
	$scope.$on('onOpenSocket', function(event, data){
		$rootScope.socketOpen = true;
		Session.goHome();
	});
	
	/**
	 * Manejo de evento message producido por el socket
 	 * @param event
	 * @param data string JSON: Datos del mensaje
	 */
	$scope.$on('onMessageSocket', function(event, data){
		$scope.$broadcast("onMessage", data);
	});
	
	/**
	 * Manejo de evento error general
	 * @param data string JSON
	 *		message: Descripcion del error
	 */
	$scope.$on('onError', function(event, data){
		var response = JSON.parse(data);
		alert(response.message);
		$rootScope.socketOpen = false;
		Session.goHome();
	});
	
	/**
	 * Manejo de evento mensaje general
	 * @param data string JSON: Datos del mensaje
	 */
	$scope.$on('onMessage', function(event, data){
		var response = JSON.parse(data);

		action = getActionFromMessage(response);
		
		switch(action){
			case "createSession":
				Session.create(response.session);
			break;
			
			case "accountCreated":
				alert("cuenta creada satisfactoriamente");
				Session.goHome();
			break;
			
			case "userSessionModified":
				alert("usuario modificado satisfactoriamente");
				Session.goHome();
			break;
			
			case "destroySession":
				Session.destroy();
			break;
			
			case "goHome":
				Session.goHome();
			break;
		}
	});
	
}]);
