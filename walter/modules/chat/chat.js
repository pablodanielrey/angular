var app = angular.module('mainApp');

app.controller('ChatCtrl', function($rootScope, $scope, WebSocket, Utils) {

  var delay = 1000;
  $scope.new_message = {'text':'escriba algo'};
  $scope.messages = [];
  $scope.cclass = '';

  $scope.$on('ChatMessage', function(event,data) {
    var message = {'data':data}
    $scope.messages.push(message);
    if ($scope.cclass == 'chat-my-message') {
      $scope.cclass = 'chat-hide';
    } else {
      $scope.cclass = 'chat-show';
    }
  });


  $scope.sendMessage = function() {
    var msg = {
      'id':Utils.getId(),
      'action':'sendEventToClients',
      'type':'ChatMessage',
      'data': $scope.new_message.text
    };
    WebSocket.send(JSON.stringify(msg));
    $scope.cclass = 'chat-my-message';
  }

  $scope.showChat = function() {
    $scope.cclass = 'chat-show';
  }
});
