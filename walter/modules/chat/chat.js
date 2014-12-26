var app = angular.module('mainApp');

app.controller('ChatCtrl', function($rootScope, $scope, WebSocket, Utils) {

  $scope.new_message = {'text':'escriba algo'};
  $scope.messages = [];

  $scope.$on('ChatMessage', function(event,data) {
    var message = {'data':data}
    $scope.messages.push(message);
  });


  $scope.sendMessage = function() {
    var msg = {
      'id':Utils.getId(),
      'action':'sendEventToClients',
      'type':'ChatMessage',
      'data': $scope.new_message.text
    };
    WebSocket.send(JSON.stringify(msg));
  }
});
