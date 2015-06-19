
var app = angular.module('mainApp');
/**
 * Controlador para realizar login
 * @param $scope Scope
 * Supone la existencia de un elemento padre que maneja los eventos dontShowMessage y showMessage para administrar mensajes
 */
app.controller("LoginCtrl", ['$rootScope','$scope', '$window', 'Session','Credentials','Notifications',
	function($rootScope,$scope, $window, Session, Credentials, Notifications) {

		$scope.user = {
			username: '',
			password: ''
		};

		$scope.hasToLogin = function() {
			return (!Credentials.isLogged());
		}

		$scope.myFunc= function() {
			console.log("Enterr");
		}

		$scope.login = function() {
			/*
				bug de angular.
				http://stackoverflow.com/questions/14965968/angularjs-browser-autofill-workaround-by-using-a-directive
			*/
			$scope.$broadcast("autofill:update");

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
							username: creds.username,
							password: creds.password
						}
					}

					Session.create(s.session, data);
					$scope.user.username = '';
					$scope.user.password = '';

					$window.location.href = "/index.html";
				},
				function(error) {
					Notifications.message(error);
				});

		};

}]);
