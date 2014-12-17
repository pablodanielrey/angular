
app.factory('WebSocket', ["$rootScope", function($rootScope){
		
	var socket = new WebSocket("ws://localhost:8000");
	
	socket.onopen = function(msg){
		$rootScope.$apply(function () {
			var data = {
				"action" : "openSocket"
			}
			$rootScope.$broadcast("onEvent", JSON.stringify(data));
		});
	}
	
	socket.onmessage = function(msg){
		$rootScope.$apply(function () {
			$rootScope.$broadcast("onEvent", msg.data);
		});
	}
	
	socket.onerror = function(msg){
		$rootScope.$apply(function (){
			var data = {
				"action" : "error",
				"message" : "error websocket",
			}
			$rootScope.$broadcast("onEvent", JSON.stringify(data));
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
