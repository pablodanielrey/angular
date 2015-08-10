angular
    .module('mainApp')
    .controller('DigestoCtrl',DigestoCtrl)

DigestoCtrl.$inject = ['$rootScope','$scope','$location','$timeout','$wamp','Login'];

function DigestoCtrl($rootScope,$scope,$location,$timeout,$wamp,Login) {

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
    // $wamp.open();
    $scope.initialize();
  });


}
