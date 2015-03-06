var app = angular.module('mainApp');

app.controller('MessagesCtrl',function($scope,$timeout) {

  $scope.visible = false;
  $scope.messages = ['Error creando la contraseña','No se pudo enviar el mail'];

  $scope.$on('ShowMessageEvent',function(event,data) {
    $scope.messages.push(data);
    $scope.visible = true;
    $timeout(function() {
      $scope.visible = false;
    }, 5000);
  });


  $scope.isVisible = function() {
    return $scope.visible;
  }


});
