
var app = angular.module('mainApp');


app.controller('ChangePasswordCtrl', function($rootScope, $scope, $routeParams, $location, $timeout, $window, Messages, Utils, Session, Credentials, Notifications) {

  $scope.user = {};
  $scope.cp = {};

  $scope.clear = function() {
    $scope.user.username = '';
    $scope.user.newPassword = '';
    $scope.user.newPasswordRepeat = '';
  }

  $scope.changePassword = function() {

    if (($scope.cp.hash != undefined) && ($scope.cp.hash != null)) {
      Credentials.changePasswordWithHash($scope.user,$scope.cp.hash,
        function(ok) {
          Notifications.messageWithCallback('Clave cambiada exitósamente');
          $timeout(function() {
            //$location.path('/');
            $window.location.href='/';
          },1000);

        },
        function(error) {
          Notifications.message(['Ocurrió un error cambiando su clave','Por favor llame al 4236769 interno 123']);
        });
    } else {
      Credentials.changePassword($scope.user,
        function(ok) {
          Notifications.message('Clave cambiada exitósamente');
        },
        function(error) {
          Notifications.message(['Ocurrió un error cambiando su clave','Por favor llame al 4236760 interno 123']);
        });
    }
  }

  $scope.$on('UserSelectedEvent', function(e,id) {
    
  });

  $scope.clear();

  // obtengo los datos de la sesion o del hash
  if ($routeParams['hash'] != undefined) {

    $scope.user.username = $routeParams['username'];
    $scope.cp.hash = $routeParams['hash'];

  } else {

    var s = Session.getCurrentSession();
    $scope.user.username = s.login.username;
    $scope.cp.hash = null;

  }

});
