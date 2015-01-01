var app = angular.module('mainApp');

app.controller('EditProfileCtrl', function($scope, Session, Messages, Utils, Users) {

  $scope.user = {};

  $scope.$on('UserSelectedEvent', function(event,data) {
    $scope.user = {};
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

    $scope.user = {};
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
    Users.findUser($scope.user.id,
      function(user) {
        $scope.user = user;
      },
      function(error) {
        alert(error);
      });
  }


});
