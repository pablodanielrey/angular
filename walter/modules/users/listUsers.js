
/*
  Lista los usuarios del sistema.

  eventos :

    UserSelectedEvent

*/

var app = angular.module('mainApp');

app.controller('ListUsersCtrl',function($rootScope, $scope, Messages, Utils, Session) {

  $scope.users = [];
  $scope.selected = '';

  $scope.isSelected = function(id) {
    return ($scope.selected == id);
  }

  $scope.selectUser = function(id) {
    $scope.selected = id;
    $rootScope.$broadcast('UserSelectedEvent',id);
  }

  $scope.listUsers = function() {
    var  msg = {
      id: Utils.getId(),
      action: 'listUsers',
      session: Session.getSessionId()
    };
    Messages.send(msg, function(response) {
      $scope.users = [];

      if (response.error != undefined) {
        alert(response.error);
        return;
      }

      $scope.users = response.users;
    });
  };

  $scope.listUsers();

});
