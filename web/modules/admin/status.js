
var app = angular.module('mainApp')

app.controller('StatusCtrl',function($scope, Utils, Session, Messages) {

  $scope.status = {'sessions':[]};

  $scope.$on('StatusChangedEvent',function(e,data) {
    $scope.updateStatus();
  })


  $scope.updateStatus = function() {
    var msg = {
      id: Utils.getId(),
      session: Session.getSessionId(),
      action: 'getStatus'
    }
    Messages.send(msg,
      function(response) {
        $scope.status = { 'sessions':response.sessions};
      },
      function(error) {
        //alert(error);
      });
  }

  $scope.updateStatus();

});
