
var app = angular.module('mainApp');

app.controller('ConnectionCtrl', function($scope, WebSocket) {

  $scope.connected = false;

  $scope.$on('onSocketOpened', function(event,data) {
    $scope.connected = true;
  });

  $scope.$on('onSocketClosed', function(event,data) {
    $scope.connected = false;
  });

  $scope.isConnected = function() {
    return $scope.connected;
  };

  $scope.connect = function() {
    WebSocket.registerHandlers();
  }

})
