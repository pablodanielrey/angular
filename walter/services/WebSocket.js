var app = angular.module('mainApp');

app.service('WebSocket', function($rootScope, Config) {

		$rootScope.states = { CONNECTING:0, OPEN:1, CLOSING:2, CLOSED:3 };
		$rootScope.socket = null;

		this.registerHandlers = function() {

			// abro el socket y registro los handlers de los eventos.
			var url = Config.getWebsocketConnectionUrl();
			console.log(url);
			$rootScope.socket = new WebSocket(url);
			$rootScope.socket.onopen = function(msg){
				console.log('socket conectado');
				setTimeout(function() {
					$rootScope.$apply(function () {
						$rootScope.$broadcast("onSocketOpened", msg);
					});
				},0);
			}

			$rootScope.socket.onclose = function(msg) {
				$rootScope.socket = null;
				setTimeout(function() {
						$rootScope.$apply(function() {
							$rootScope.$broadcast('onSocketClosed',msg);
						});
					},0);
			}

			$rootScope.socket.onmessage = function(msg) {
				setTimeout(function() {
					$rootScope.$apply(function () {
						$rootScope.$broadcast("onSocketMessage", msg.data);
					});
				}, 0);
			}

			$rootScope.socket.onerror = function(msg){
				setTimeout(function() {
					$rootScope.$apply(function () {
						$rootScope.$broadcast("onSocketError", JSON.stringify(msg));
					});
				},0);
			}

		}

		this.isConnected = function() {
			if($rootScope.socket == null){
				return false;
			}
			
			return ($rootScope.socket.readyState == 1);
			
		}
		
		this.isConnecting = function() {
			if($rootScope.socket == null){
				return false;
			}
			
			return ($rootScope.socket.readyState == 0);
		}

		this.send = function(msg) {
			if(this.isConnected()){
				$rootScope.socket.send(msg);
			} else {
				$rootScope.$on('onSocketOpened',function(event,data){
					$rootScope.socket.send(msg);
			    });
			} 
		}

		this.close = function() {
			if ($rootScope.socket == null) {
				return;
			}
			$rootScope.socket.close();
			$rootScope.socket = null;
		}

//		this.registerHandlers();

});
