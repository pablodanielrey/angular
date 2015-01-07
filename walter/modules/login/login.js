
var app = angular.module('mainApp');
/**
 * Controlador para realizar login
 * @param $scope Scope
 * Supone la existencia de un elemento padre que maneja los eventos dontShowMessage y showMessage para administrar mensajes
 */
app.controller("LoginCtrl", function($rootScope,$scope, Session, Credentials) {

		$scope.user = {
			username: '',
			password: ''
		};

		$scope.hasToLogin = function() {
			return (!Credentials.isLogged());
		}

		$scope.login = function() {

			var creds = {
				username: $scope.user.username,
				password: $scope.user.password
			};


			Credentials.login(creds,
				function(s) {
					var data = {
						session_id: s.session,
						user_id: s.user_id,
						login: {
							username: creds.username
						}
					}

					Session.create(s.session, data);
					$scope.user.username = '';
					$scope.user.password = '';
				},
				function(error) {
					alert(error);
				});
		};

});
