
var app = angular.module('mainApp');


app.controller('ConfirmAccountRequestCtrl',function($scope,$rootScope,$routeParams,$timeout,Utils,Messages,WebSocket) {

  $scope.message = '';
  $scope.hash = $routeParams['hash'];

  $scope.sendConfirmation = function() {
    var msg = {
      id: Utils.getId(),
      action: 'confirmAccountRequest',
      hash: $scope.hash
    };

    Messages.send(msg, function(response) {
      if (response.ok == undefined) {
        $scope.message = 'error creando el pedido';
        $scope.hash = '';
      } else {
        // aca se muestra un mensaje pero se podría mostrar un div oculto con el mensaje bien formateado.
        $scope.message = 'Pedido de cuenta creado correctamente, se confirmará mediante un mail a su dirección de correo';
        $scope.hash = '';
      }
    });
  }

  $timeout(function() {
    if ($scope.hash == undefined || $scope.hash == '') {
      $scope.message = 'error';
      return;
    }

    if (!WebSocket.isConnected()) {
      $rootScope.$on('onSocketOpened',function(event,data) {
        $scope.sendConfirmation();
      });
    } else {
      $scope.sendConfirmation();
    }
  },20);


});
