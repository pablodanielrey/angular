
var app = angular.module('mainApp');

app.controller('LogoutCtrl', function($scope, Session, Messages, Utils) {

  $scope.logout = function() {

    var msg = {
      id: Utils.getId(),
      action: 'logout',
      session: Session.getSessionId()
    };

    Messages.send(msg, function(response) {

      if (response.ok != undefined) {
        Session.destroy();
        $scope.$emit('logoutOk','');
        $location.path('/');
      }

    });

  };

  $scope.logout();

});
