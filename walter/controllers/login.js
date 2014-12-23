
var app = angular.module('mainApp');
/**
 * Controlador para realizar login
 * @param $scope Scope
 * Supone la existencia de un elemento padre que maneja los eventos dontShowMessage y showMessage para administrar mensajes
 */
app.controller("LoginCtrl", function($rootScope, $scope, $location, WebSocket, Session){

		$scope.user = { username: '', password: ''};

		var ids = new Array();

		/**
		 * autenticar usuario
		 */
		$scope.login = function() {
			var id =  (Math.floor((Math.random() * 1000000000) + 1)).toString();
			ids[id] = true;

			var data = {
				"id" : id,
				"user" : $scope.user.username,
				"password" : $scope.user.password,
				"action" : "login",
			}

			WebSocket.send(JSON.stringify(data));
		};

		/**
		 * Manejo de evento message producido por el socket
	 	 * @param event
		 * @param data string JSON: Datos del mensaje
		 */
		$scope.$on('onMessage', function(event, response) {

			if(ids[response.id] == undefined) {
				// no es una respuesta mia
				return;
			}

			if(response.error != undefined){
				var data = {
					"message" : response.error,
				}
				$rootScope.$broadcast("onAppError", JSON.stringify(data));
				return;
			}

			if(response.session != undefined) {
				// logueo al usuario con el id de sesion retornado por el server.
				Session.create(response.session);
				$scope.$emit('loginOk','');
				return;
			}
	});
});
