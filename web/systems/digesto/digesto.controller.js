angular
    .module('mainApp')
    .controller('DigestoCtrl',DigestoCtrl)

DigestoCtrl.$inject = ['$rootScope','$scope','$location','$window','$wamp','Login'];

function DigestoCtrl($rootScope,$scope,$location,$window,$wamp,Login) {

  $scope.initialize = initialize;

  $scope.$on('$viewContentLoaded', function(event) {
    $scope.initialize();
  });

  function initialize() {
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


}
