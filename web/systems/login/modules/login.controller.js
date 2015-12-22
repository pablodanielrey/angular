
angular
  .module('mainApp')
  .controller('LoginCtrl',LoginCtrl);

LoginCtrl.$inject = ['$rootScope','$scope', '$location','$window','Notifications','Login'];

function LoginCtrl($rootScope, $scope, $location, $window, Notifications, Login) {

    var vm = this;

    $scope.model = {
			username: '',
			password: '',
      openConnection: false
    }

    $scope.view = {
      classConnection: 'verServerDesconectado'
    }

    $scope.initialize = function() {

    }

    $scope.$on('$viewContentLoaded', function(event) {
      $scope.initialize();
    });

    $scope.$on('wampOpenEvent', function(event) {
      $scope.model.openConnection = true;
      $scope.view.classConnection = 'verServerConectado';
    });

    $scope.$on('wampCloseEvent', function(event) {
      $scope.model.openConnection = false;
      $scope.view.classConnection = 'verServerDesconectado';
    });

		$scope.hasToLogin = function() {
			return (!Login.isLogged());
		}

		$scope.login = function() {
			/*
				bug de angular.
				http://stackoverflow.com/questions/14965968/angularjs-browser-autofill-workaround-by-using-a-directive
			*/
			$scope.$broadcast("autofill:update");

      Login.login($scope.model.username, $scope.model.password,
        function(sid) {
            // usuario logueado correctamente
            $window.location.href = "/index.html";

        }, function(err) {
            Notifications.message(err);
        });

		};

};
