
var app = angular.module('mainApp');


app.controller('ResetPasswordCtrl', function($scope) {

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
        alert('Se ha enviado un mail de confirmación a sus cuentas de email. Por favor chequee bandeja de entrada y correo no deseado');
      },
      function(error) {
        alert(error);
      });
  }

  $scope.clearUsername();

});
