
var app = angular.module('mainApp');


app.controller('ResetPasswordCtrl', function($rootScope, $scope, Credentials, Notifications,$window) {

  $scope.user = { username:'' };

  $scope.clearUsername = function() {
    $scope.user = { username:'' };
  }

  $scope.resetPassword = function() {

    if (($scope.user.username == null) || ($scope.user.username == '')) {
      return;
    }

    Credentials.resetPassword($scope.user.username,
      function(ok) {
        Notifications.message(['Se ha enviado un mail de confirmación a sus cuentas de email','Por favor chequee bandeja de entrada y correo no deseado']);
      },
      function(error) {
        Notifications.message(['Se ha producido un error al resetear su clave','Por favor llame a 4236769 interno 123']);
      });
  }

  $scope.back = function() {
    $window.location.href = "/systems/login/indexLogin.html";
  }

});
