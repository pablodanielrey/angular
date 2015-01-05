
var app = angular.module('mainApp');


app.controller('ResetPasswordCtrl', function($scope, Utils, Messages) {

  $scope.user = { username:'' };

  $scope.clearUsername = function() {
    $scope.user = { username:'' };
  }

  $scope.resetPassword = function() {

    if (($scope.user.username == null) || ($scope.user.username == '')) {
      return;
    }

    var msg = {
      id: Utils.getId(),
      action: 'resetPassword',
      username: $scope.user.username,
      url: document.URL
    };
    Messages.send(msg,
      function(ok) {
        alert('Se ha enviado un mail de confirmación a sus cuentas de email. Por favor chequee bandeja de entrada y correo no deseado');
      },
      function(error) {
        alert(error);
      });
  }

  $scope.clearUsername();

});
