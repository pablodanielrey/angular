
/*
  Lista los usuarios del sistema.

  eventos disparados :

    UserSelectedEvent


  eventos escuchados :

    UserUpdatedEvent

*/

var app = angular.module('mainApp');

app.controller('ListUsersCtrl',function($rootScope, $scope, $timeout, Session, Users) {

  $scope.users = [];
  $scope.selected = '';
  $scope.updating = '';

  $scope.isUpdated = function(id) {
    return ($scope.updating == id);
  }

	/**
	 * UserUpdatedEvent. Al actualizar un usuario:
	 *		Se modifica el usuario actualizado dentro de la lista de usuarios
	 *		Si no se encuentra el usuario actualizado, se listan nuevamente todos los usuarios
	 */
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
				$scope.users[pos].fullname =  $scope.users[pos].name + " " +  $scope.users[pos].lastname; //definir dato fullname compuesto por el name y el lastname
			},
	
			function(error) {
				$scope.listUsers();
			}
		);
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
        for (i = 0; i < users.length; i++) {
	        $scope.users[i].fullname = users[i].name + " " + users[i].lastname;
		}
        
      },
      function(error) {
        alert(error);
      });
  };
  
	$timeout(function() {
		$scope.listUsers();
	},0);
});
