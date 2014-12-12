
app.controller("LoginController", ["$scope", "WebSocket", function($scope, WebSocket) {
	var socketOpen = false;
	
	$scope.authenticate = function(){
		if(!socketOpen) {
			alert("no es posible realizar la autenticacion");
			return;
		}
		
		var data = {
			"user" : $scope.user,
			"password" : $scope.password,
		}
		
		WebSocket.send(data.toString());
	};
	
	$scope.$on('socketOnOpen', function(event, msg) { 
		socketOpen = true;
	});
	
	$scope.$on('socketOnMessage', function(event, msg) { 
		$scope.authentication = msg.data
	});

}]); 
