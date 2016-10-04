
angular
  .module('mainApp')
  .controller('IndexCtrl',IndexCtrl);

IndexCtrl.$inject = ['$rootScope','$scope','$wamp','$window', 'Notifications', 'Login'];

function IndexCtrl($rootScope, $scope, $wamp, $window, Notifications, Login) {

    $scope.model = {
      hideMenu: false
    };
    $scope.styleMenu = 'full';

    $scope.hideMenu = function() {
      return $scope.model.hideMenu;
    }

    $scope.$watch(function() { return $window.innerWidth; }, function(o,n) {
        if ($window.innerWidth <= 720) {
          $scope.styleMenu = 'celular';
        } else {
          $scope.styleMenu = 'full';
        }
    });

    $scope.initialize = function() {
      $scope.styleMenu = 'full';
      Login.getSessionData()
      .then(function(s) {
        console.log(s);
      }, function(err) {
        $window.location.href = "/systems/login/index.html";
      })
    }

    $scope.$on('$viewContentLoaded', function(event) {
      $scope.initialize();
    });

};
