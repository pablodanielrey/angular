
angular
  .module('fce')
  .controller('IndexCtrl',IndexCtrl);

IndexCtrl.$inject = ['$rootScope','$scope','$wamp','$window', 'Notifications', 'Login'];

function IndexCtrl($rootScope, $scope, $wamp, $window, Notifications, Login) {

    $scope.model = {
      hideMenu: false
    };

    $scope.hideMenu = function() {
      return $scope.model.hideMenu;
    }


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
