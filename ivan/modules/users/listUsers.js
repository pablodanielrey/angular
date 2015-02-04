
/*
  Lista los usuarios del sistema.

  eventos disparados :

    UserSelectedEvent


  eventos escuchados :

    UserUpdatedEvent

*/

var app = angular.module('mainApp');

app.controller('ListUsersCtrl',function($rootScope, $scope, $log, Session, Users) {

  $scope.users = [];
  $scope.selected = '';
  $scope.updating = '';

  $scope.isUpdated = function(id) {
    return ($scope.updating == id);
  }

  $scope.$on('UserUpdatedEvent',function(event,id) {

    $scope.updating = id;

    var found = null;
    var pos = -1;

    // busco el usuario dentro de la lista de usuarios
    for (var i = 0; i < $scope.users.length; i++) {
      var user = $scope.users[i];
      if (user.id == id) {
        found = user;
        pos = i;
        break;
      }
    }

    if (found == null) {
      $scope.listUsers();
      return;
    }

    // busco los datos del usuario actualizado, en caso de error busco nuevamente la lista.
    Users.findUser(found.id,
      function(user) {
        $scope.users[pos] = user;
      },
      function(error) {
        $scope.listUsers();
      });
  });

  $scope.isSelected = function(id) {
    return ($scope.selected == id);
  }


	/**
	 * Seleccionar usuario en funcion del id
	 */
	$scope.selectUser = function(id) {
		$scope.selected = id;

		var s = Session.getCurrentSession();
		s.selectedUser = id;
		Session.saveSession(s);

		$rootScope.$broadcast('UserSelectedEvent',id);
	}

  $scope.listUsers = function() {
    Users.listUsers(
      function(users) {
        $scope.users = users;
      },
      function(error) {
        alert(error);
      });
  };

  $scope.listUsers();

});
