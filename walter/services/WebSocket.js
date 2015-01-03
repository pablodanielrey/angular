var app = angular.module('mainApp');

app.service('WebSocket', function($rootScope) {

		this.registerHandlers = function() {

			// abro el socket y registro los handlers de los eventos.
			this.socket = new WebSocket("ws://192.168.0.100:8001");

			this.socket.onopen = function(msg){
				$rootScope.$apply(function () {
					$rootScope.$broadcast("onSocketOpened", msg);
				});
			}

			this.socket.onclose = function(msg) {
				this.socket = null;
				$rootScope.$apply(function() {
					$rootScope.$broadcast('onSocketClosed',msg);
				});
			}

			this.socket.onmessage = function(msg){
				$rootScope.$apply(function () {
					$rootScope.$broadcast("onSocketMessage", msg.data);
				});
			}

			this.socket.onerror = function(msg){
				$rootScope.$apply(function () {
					$rootScope.$broadcast("onSocketError", JSON.stringify(msg));
				});
			}

		}

		this.send = function(msg){
				this.socket.send(msg);
		}

		this.close = function(){
			this.socket.close();
			this.socket = null;
		}

		this.registerHandlers();

});
