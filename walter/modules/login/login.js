
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
			var sid = Session.getSessionId();
			if (sid == null) {
				return false;
			}
			var s = Session.getSession(sid);
			if (s == null) {
				return false;
			}
			return ((s.user_id != undefined) && (s.user_id != null));
		}

		$scope.login = function() {
			var msg = {
				"id" : Utils.getId(),
				"user" : $scope.user.username,
				"password" : $scope.user.password,
				"action" : "login"
			}

			Messages.send(msg, function(response) {

				if(response.session == undefined) {
					$scope.$emit('loginError');
					return;
				}


				var data = {
					session_id: response.session,
					user_id: response.user_id
				}
				Session.create(response.session, data);
				$scope.user.username = '';
				$scope.user.password = '';
				$scope.$emit('loginOk','');

			});

		};

});
