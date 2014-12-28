var app = angular.module('mainApp');

app.controller('ChatCtrl', function($rootScope, $scope, WebSocket, Utils) {

  $scope.new_message = {'text':''};
  $scope.chatVisible = false;
  $scope.maximized = true;
  $scope.messages = [];

  $scope.$on('ChatMessage', function(event,data) {
    var message = {'text':data}
    $scope.messages.push(message);

    if (!$scope.chatVisible) {
      $scope.chatVisible = true;
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

    $scope.new_message.text = '';
  }

  $scope.isChatVisible = function() {
    return $scope.chatVisible;
  }

  $scope.isMaximized = function() {
    return $scope.maximized;
  }

  $scope.showChat = function() {
    $scope.chatVisible = true;
  }

  $scope.closeChat = function() {
    $scope.chatVisible = false;
  }

  $scope.minimizeChat = function() {
    $scope.maximized = false;
  }

  $scope.maximizeChat = function() {
    $scope.maximized = true;
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
