var app = angular.module('mainApp');

app.controller('EditProfileCtrl', function($scope, Session, Messages, Utils) {

  $scope.user = {};

  $scope.findUserData = function(id, callbackOk, callbackError) {
    var msg = {
      id: Utils.getId(),
      session: Session.getSessionId(),
      action: 'findUser',
      user: { id: id}
    }
    Messages.send(msg, function(response) {
      if (response.error != undefined) {
        callbackError(response.error);
      } else {
        callbackOk(response.user);
      }
    });
  }

  $scope.$on('UserSelectedEvent', function(event,data) {

    $scope.user = {};
    $scope.findUserData(data,
      function(user) {
        $scope.user = user;
      },
      function(error) {
        alert(error);
      });

  });


  $scope.update = function() {
    var msg = {
      id: Utils.getId(),
      session: Session.getSessionId(),
      action: 'updateUser',
      user: $scope.user
    };
    Messages.send(msg,function(response) {
      if (response.error != undefined) {
        alert(response.error);
        return
      }
    });
  }

  $scope.cancel = function() {
    $scope.user = {};
    $scope.findUserData(data,
      function(user) {
        $scope.user = user;
      },
      function(error) {
        alert(error);
      });
  }


});
