
var app = angular.module('mainApp');


app.controller('ChangePasswordCtrl', function($rootScope, $scope, $routeParams, $location, $timeout, $window, Session, Credentials, Notifications) {

  $scope.user = {};
  $scope.cp = {};

  $scope.clear = function() {
    $scope.user.username = '';
    $scope.user.newPassword = '';
    $scope.user.newPasswordRepeat = '';
  }

  $scope.changePassword = function() {

    if (($scope.cp.hash != undefined) && ($scope.cp.hash != null)) {

      if ($scope.user.newPassword != $scope.user.newPasswordRepeat) {
        Notifications.message(['Las claves son distintas']);
        return;
      }

      var creds = {
        username: $scope.user.username,
        password: $scope.user.newPassword
      };

      Credentials.changePasswordWithHash(creds, $scope.cp.hash,
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

      var sid = Session.getSessionId();
      if (sid == null) {
        Notifications.message(['Debe ingresar al sistema con la clave actual para poder cambiar a una nueva clave']);
        return;
      }

      Credentials.changePassword(sid, $scope.user,
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
    if (s == undefined || s == null) {
      $scope.clear();
    } else {
      $scope.user.username = s.login.username;
      $scope.cp.hash = null;
    }
  }

});
