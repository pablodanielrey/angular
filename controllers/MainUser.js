
app.controller("MainUserController", ["$rootScope", "$scope", "$cookies", "$location", "WebSocket", function($rootScope, $scope, $cookies, $location, WebSocket) {
	$rootScope.socketOpen = false;
	$location.path("/start");
	
	$scope.$on('onEvent', function(event, data){

		var response = JSON.parse(data);

		switch(response.action){
		
			case "goHome":
				if(($cookies.fceSession != undefined) 
				&& ($cookies.fceSession != "0") 
				&& ($cookies.fceSession != null)
				&& ($cookies.fceSession != false)){
					$location.path("/home");				
				} else {
					$location.path("/login");	
				}
			break;
			
			case "error":
				alert(response.message);
				$cookies.fceSession = "0";
				var data = {"action" : "goHome"}
				$scope.$broadcast("onEvent", JSON.stringify(data));
			break;
			
			case "openSocket":
				$rootScope.socketOpen = true;
				var data = {"action" : "goHome"	}
				$scope.$broadcast("onEvent", JSON.stringify(data));
			break;
			
			case "closeSocket":
				$rootScope.socketOpen = false;
			break;
			
			case "authenticate":	
				var data = {
					"user" : response.user,
					"password" : response.password,
					"action" : "login",
				}
				
				WebSocket.send(JSON.stringify(data));
			break;
			
			case "getUserSession":
				var data = {
					"session" : $cookies.fceSession,
					"action" : "getUserSession",
				}
				
				WebSocket.send(JSON.stringify(data));
			break;
			
			case "userSessionData":
				var data = {
					"session" : $cookies.fceSession,
					"name" : response.user,
					"lastname" : response.lastname,
					"dni" : response.dni,
					"mail" : response.mail,
				}
				
				$scope.$broadcast("userData", JSON.stringify(data));
			break;
			
			case "createSession":
				$cookies.fceSession = response.session;
				var data = {"action" : "goHome"}
				$scope.$broadcast("onEvent", JSON.stringify(data));
			break;
			
			case "destroySession":
				$cookies.fceSession = "0";
				var data = {"action" : "goHome"}
				$scope.$broadcast("onEvent", JSON.stringify(data));
			break;

			default:
				var data = {"action" : "destroySession"}
				$scope.$broadcast("onEvent", JSON.stringify(data));
			break;
		}
	});
}]);
