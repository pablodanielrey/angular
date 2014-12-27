var app = angular.module('mainApp');

app.controller('ChatCtrl', function($rootScope, $scope, WebSocket, Utils) {


  remove = function(array, element) {
    for (var i = 0; i < array.length; i++) {
      if (array[i] == element) {
        array.slice(i,1);
        break;
      }
    }
  }

  var delay = 1000;
  $scope.new_message = {'text':'escriba algo'};
  $scope.messages = [];
  $scope.cclass = [];
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

    remove($scope.cclass,'chat-show');
    remove($scope.cclass,'chat-hide');
    $scope.cclass.push('chat-my-message');
    $scope.cmessages = '';
  }

  $scope.showChat = function() {
    remove($scope.cclass,'chat-hide');
    $scope.cclass.push('chat-show');
  }

  $scope.hideChat = function() {
    remove($scope.cclass,'chat-show');
    $scope.cclass.push('chat-hide');
  }


  $scope.closeChat = function() {
    $scope.cmessages = '';
    $scope.hideChat();
  }

  $scope.maximizeChat = function() {
    remove($scope.cclass,'chat-minimize');
    $scope.cclass.push('chat-maximize');
  }

  $scope.minimizeChat = function() {
    remove($scope.cclass,'chat-maximize');
    $scope.cclass.push('chat-minimize');
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
