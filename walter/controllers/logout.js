
var app = angular.module('mainApp');

app.controller('LogoutCtrl', function($scope, Session, WebSocket, Utils) {

  var ids = new Array();

  $scope.logout = function() {
    var id = Utils.getId();
    var session = Session.getSessionId();
    var msg = {'id':id, 'action':'logout', 'session':session};

    ids[id] = true;
    WebSocket.send(JSON.stringify(msg));
  };

  $scope.$on('onMessage', function(event, data) {

    if (ids[data.id] == undefined) {
      return;
    }

    if (data.ok == undefined) {
      return;
    }

    Session.destroy();
    $scope.$emit('routeEvent','#/index');
  });

});
