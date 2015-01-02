
var app = angular.module('mainApp');
/**
 * Controlador para realizar login
 * @param $scope Scope
 * Supone la existencia de un elemento padre que maneja los eventos dontShowMessage y showMessage para administrar mensajes
 */
app.controller("LoginCtrl", function($rootScope, $scope, $location, Messages, Session, Utils){

		$scope.user = {
			username: '',
			password: ''
		};


		$scope.isLogged = function() {
			return Session.isLogged();
		}

		$scope.login = function() {
			var msg = {
				"id" : Utils.getId(),
				"user" : $scope.user.username,
				"password" : $scope.user.password,
				"action" : "login",
			}

			Messages.send(msg, function(response) {

				if(response.session != undefined) {
					// logueo al usuario con el id de sesion retornado por el server.

					var data = {
						user_id: response.user_id
					}

					Session.create(response.session, data);
					$scope.$emit('loginOk','');
				} else {
					$scope.$emit('loginError','');
				}

			});

		};

});
