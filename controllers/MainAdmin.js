
app.controller("MainAdminController", ["$rootScope", "$scope", "$location", "WebSocket", "Session", function($rootScope, $scope, $location, WebSocket, Session) {
	$rootScope.socketOpen = false;
	$location.path("/loading");

	/**
	 * Manejo de evento apertura de socket
	 * @param data string JSON: Datos del mensaje 
	 */
	$scope.$on('onOpenSocket', function(event, data){
		$location.path("/listCreateAccount");
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
	 * Manejo de evento error de aplicacion
	 * @param data string JSON
	 *		message: Descripcion del error
	 */
	$scope.$on('onAppError', function(event, data){
		var response = JSON.parse(data);
		alert(response.message);
	});
	
	/**
	 * Manejo de evento mensaje de aplicacion
	 * @param data string JSON
	 *		message: Descripcion del error
	 */
	$scope.$on('onAppMessage', function(event, data){
		var response = JSON.parse(data);
		alert(response.message);
	});
	

	
}]);
