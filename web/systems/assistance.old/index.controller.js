
angular
  .module('mainApp')
  .controller('IndexCtrl',IndexCtrl);

IndexCtrl.$inject = ['$rootScope','$scope','$wamp','$window', 'Notifications', 'Login'];

function IndexCtrl($rootScope, $scope, $wamp, $window, Notifications, Login) {

    var vm = this;

    $scope.model = {
    }

    $scope.initialize = function() {
      if (!Login.isLogged()) {
        $window.location.href = "/systems/login/index.html";
      }

      Login.validateSession(
        function(v) {
          if (!v) {
            $window.location.href = "/systems/login/index.html";
          }
        },
        function(err) {
          Notifications.message(err);
      })
    }

    $scope.$on('$viewContentLoaded', function(event) {
      $scope.initialize();
    });

};
