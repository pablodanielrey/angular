
app.factory('WebSocket', ["$rootScope", function($rootScope){
		
	var socket = new WebSocket("ws://echo.websocket.org");
	
	socket.onopen = function(msg){
		$rootScope.$apply(function () {
			$rootScope.$broadcast("socketOnOpen", msg);
		});
	}
	
	socket.onmessage = function(msg){
		$rootScope.$apply(function () {
			$rootScope.$broadcast("socketOnMessage", msg);
		});
	}
	
	socket.onerror = function(msg){
		$rootScope.$apply(function (){
			$rootScope.$broadcast("socketOnError", msg);
		});
	}
	
	var factory = {};
	
	factory.send = function(msg){
		socket.send(msg);	
	}
	
	factory.close = function(){
		socket.close();
	}
	
	return factory;
}]);
