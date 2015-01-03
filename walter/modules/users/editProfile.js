var app = angular.module('mainApp');

app.controller('EditProfileCtrl', function($scope, Session, Messages, Utils, Users) {

  $scope.user = {};

  $scope.clearUser = function() {
    $scope.user = { id:'', name:'', lastname:'', dni:'', telephone:'', genre:'' }
  }

  $scope.$on('UserSelectedEvent', function(event,data) {
    $scope.clearUser();
    Users.findUser(data,
      function(user) {
        $scope.user = user;
      },
      function(error) {
        alert(error);
      });
  });

  $scope.$on('UserUpdatedEvent', function(event,data) {

    if ($scope.user.id != data) {
      // no es el usuario seleccionado, por lo que ignoro el evento ya que estoy mostrando otro usuario.
      return;
    }

    $scope.clearUser();
    Users.findUser(data,
      function(user) {
        $scope.user = user;
      },
      function(error) {
        alert(error);
      });
  });

  $scope.update = function() {
    Users.updateUser($scope.user,
      function(ok) {
        // nada
      },
      function(error) {
        alert(error);
      });
  }

  $scope.cancel = function() {
    $scope.clearUser();
    if ($scope.user.id == undefined || $scope.user.id == null || $scope.user.id == '') {
      return;
    }
    Users.findUser($scope.user.id,
      function(user) {
        $scope.user = user;
      },
      function(error) {
        alert(error);
      });
  }

  $scope.clearUser();

});
