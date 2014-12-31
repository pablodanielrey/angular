var app = angular.module('mainApp');

app.controller('EditProfileCtrl', function($scope, Session, Messages, Utils) {

  $scope.user = {};

  $scope.$on('UserSelectedEvent', function(event,data) {

    var msg = {
      id: Utils.getId(),
      session: Session.getSessionId(),
      action: 'findUser',
      user: { id: data }
    }
    Messages.send(msg, function(response) {
      if (response.ok == undefined) {
        alert('error');
        return;
      }
      $scope.user = response.user;
    });

  });



});
