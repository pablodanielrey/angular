var app = angular.module('mainApp');

app.service('WebSocket', function($rootScope, Config) {

		var instance = this;
		this.states = { CONNECTING:0, OPEN:1, CLOSING:2, CLOSED:3 };
		this.socket = null;

		this.registerHandlers = function(ready) {

			// abro el socket y registro los handlers de los eventos.
			var url = Config.getWebsocketConnectionUrl();
			console.log(url);
			instance.socket = new WebSocket(url);

			instance.socket.onopen = function(msg){
				$rootScope.$apply(function () {
					$rootScope.$broadcast("onSocketOpened", msg);
				});
				if (ready != null) {
						ready();
				}
			}

			instance.socket.onclose = function(msg) {
				instance.socket = null;
				$rootScope.$apply(function() {
					$rootScope.$broadcast('onSocketClosed',msg);
				});
			}

			instance.socket.onmessage = function(msg){
				$rootScope.$apply(function () {
					$rootScope.$broadcast("onSocketMessage", msg.data);
				});
			}

			instance.socket.onerror = function(msg){
				$rootScope.$apply(function () {
					$rootScope.$broadcast("onSocketError", JSON.stringify(msg));
				});
			}

		}

		this.send = function(msg) {
				if ((instance.socket == null) || (instance.socket.readyState != instance.states.OPEN)) {
					instance.registerHandlers(function() {
						instance.socket.send(msg);
					});
				} else {
					instance.socket.send(msg);
				}
		}

		this.close = function() {
			if (instance.socket == null) {
				return;
			}
			instance.socket.close();
			instance.socket = null;
		}

		this.registerHandlers();

});
