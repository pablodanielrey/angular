var app = angular.module('mainApp');

app.controller('ChatCtrl', function($rootScope, $scope, WebSocket, Utils) {

  var delay = 1000;
  $scope.new_message = {'text':'escriba algo'};
  $scope.messages = [];
  $scope.cclass = '';
  $scope.cmessages = '';
  $scope.m = false;

  $scope.$on('ChatMessage', function(event,data) {
    var message = {'data':data}
    $scope.messages.push(message);
    if ($scope.cclass == 'chat-my-message') {
      $scope.hideChat();
    } else {
      $scope.showChat();
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
    $scope.cmessages = '';
  }

  $scope.showChat = function() {
    $scope.cclass = 'chat-show';
  }

  $scope.hideChat = function() {
    $scope.cclass = 'chat-hide';
  }


  $scope.closeChat = function() {
    $scope.cmessages = '';
    $scope.hideChat();
  }

  $scope.maximizeChat = function() {
    $scope.cmessages = 'chat-maximize';
  }

  $scope.minimizeChat = function() {
    $scope.cmessages = 'chat-minimize';
  }

/*
  $scope.mouseOver = function() {
    $scope.
  }


  $scope.notmoving = function() {
    $scope.m = false;
  }

  $scope.moving = function() {
    $scope.m = true;
  }
*/


});
