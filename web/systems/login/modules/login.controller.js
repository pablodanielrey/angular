
angular
  .module('mainApp')
  .controller('LoginCtrl',LoginCtrl);

LoginCtrl.$inject = ['$rootScope','$scope','$location','Notifications'];

function LoginCtrl($rootScope, $scope, $location, Notifications) {

    var vm = this;

    $scope.model = {
			username: '',
			password: ''
    }

    $scope.initialize = function() {
    }

    $scope.$on('$viewContentLoaded', function(event) {
      $scope.initialize();
    });


		$scope.hasToLogin = function() {
			return (!Credentials.isLogged());
		}

		$scope.login = function() {
			/*
				bug de angular.
				http://stackoverflow.com/questions/14965968/angularjs-browser-autofill-workaround-by-using-a-directive
			*/
			$scope.$broadcast("autofill:update");

			var creds = {
				username: $scope.model.username,
				password: $scope.model.password
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
