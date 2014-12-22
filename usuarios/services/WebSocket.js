
app.factory('WebSocket', ["$rootScope", function($rootScope){
		
	var socket = new WebSocket("ws://localhost:8001");
	
	socket.onopen = function(msg){
		$rootScope.$apply(function () {
			$rootScope.$broadcast("onOpenSocket", msg);
		});
	}
	
	socket.onmessage = function(msg){
		$rootScope.$apply(function () {
			$rootScope.$broadcast("onMessageSocket", msg.data);
		});
	}
	
	socket.onerror = function(msg){
		$rootScope.$apply(function (){
			$rootScope.$broadcast("onErrorSocket", JSON.stringify(msg));
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
