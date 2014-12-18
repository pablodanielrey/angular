
app.controller("MainUserController", ["$rootScope", "$scope", "$cookies", "$location", "WebSocket", function($rootScope, $scope, $cookies, $location, WebSocket) {
	$rootScope.socketOpen = false;
	$location.path("/start");
	
	/**
	 * Ir a la pagina de inicio que variara en funcion de si existe sesion o no
	 */
	var goHome = function(){
		if(($cookies.fceSession != undefined) 
		&& ($cookies.fceSession != "") 
		&& ($cookies.fceSession != null)
		&& ($cookies.fceSession != false)){
			$location.path("/home");				
		} else {
			$location.path("/login");	
		}
	};
	
	/**
	 * Destruir session
	 */
	var destroySession = function(){
		$cookies.fceSession = "";
		goHome();
	};
	
	
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
		goHome();
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
		$scope.goHome();
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
				$cookies.fceSession = response.session;
				goHome();
			break;
			
			case "accountCreated":
				alert("cuenta creada satisfactoriamente");
				goHome();
			break;
			
			case "userSessionModified":
				alert("usuario modificado satisfactoriamente");
				goHome();
			break;
			
			case "destroySession":
				$cookies.fceSession = "";
				goHome();
			break;
			
			case "goHome":
				goHome();
			break;
		}
	});
	
}]);
