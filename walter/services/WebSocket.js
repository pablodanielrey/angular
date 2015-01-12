var app = angular.module('mainApp');

app.service('WebSocket', function($rootScope, Config) {

		this.states = { CONNECTING:0, OPEN:1, CLOSING:2, CLOSED:3 };
		this.socket = null;

		this.registerHandlers = function() {

			// abro el socket y registro los handlers de los eventos.
			var url = Config.getWebsocketConnectionUrl();
			console.log(url);
			this.socket = new WebSocket(url);

			this.socket.onopen = function(msg){
				console.log('socket conectado');
				setTimeout(function() {
					$rootScope.$apply(function () {
						$rootScope.$broadcast("onSocketOpened", msg);
					});
				},0);
			}

			this.socket.onclose = function(msg) {
				this.socket = null;
				setTimeout(function() {
						$rootScope.$apply(function() {
							$rootScope.$broadcast('onSocketClosed',msg);
						});
					},0);
			}

			this.socket.onmessage = function(msg) {
				setTimeout(function() {
					$rootScope.$apply(function () {
						$rootScope.$broadcast("onSocketMessage", msg.data);
					});
				}, 0);
			}

			this.socket.onerror = function(msg){
				setTimeout(function() {
					$rootScope.$apply(function () {
						$rootScope.$broadcast("onSocketError", JSON.stringify(msg));
					});
				},0);
			}

		}

		this.send = function(msg) {
//				if ((instance.socket == null) || (instance.socket.readyState != instance.states.OPEN)) {
//					instance.registerHandlers(function() {
//						instance.socket.send(msg);
//					});
//				} else {
					if (this.socket == null) {
						throw "this.socket == null";
					}
					this.socket.send(msg);
//				}
		}

		this.close = function() {
			if (this.socket == null) {
				return;
			}
			this.socket.close();
			this.socket = null;
		}

//		this.registerHandlers();

});
