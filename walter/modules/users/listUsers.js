
/*
  Lista los usuarios del sistema.

  eventos disparados :

    UserSelectedEvent


  eventos escuchados :

    UserUpdatedEvent

*/

var app = angular.module('mainApp');

app.controller('ListUsersCtrl',function($rootScope, $scope, $timeout, Session, Users) {

	/**
	 * Inicializacion de variables
	 */
	$scope.model = {
		users:[], //lista de usuarios buscados
		search:"", //busqueda de usuarios
		selected:"", //usuario seleccionado
		updated:"", //usuario actualizado
		searchPromise:false, //promesa de busqueda
	}
	
	/**
	 * Buscar usuarios
	 */
	$scope.search = function(){
		if($scope.model.searchPromise){
			$timeout.cancel($scope.model.searchPromise);
		}
		
		$scope.model.searchPromise = $timeout(
			function(){
				$scope.listUsers();
			}
		,2000);
	};
	
	
	/**
	 * Listar usuarios
	 */
	$scope.listUsers = function() {
		Users.listUsers($scope.model.search,
			function(users){
				$scope.model.users = users;
			},
			function(error){
				alert(error);
			}
		);
	};
	
	/**
	 * Seleccionar usuario en funcion del id
	 */
	$scope.selectUser = function(id) {
		$scope.model.selected = id;

		var s = Session.getCurrentSession();
		s.selectedUser = id;
		Session.saveSession(s);

		$rootScope.$broadcast('UserSelectedEvent',id);
	}
	
	/**
	 * Verificar usuario seleccionado
	 */
	$scope.isSelected = function(id) {
		return ($scope.model.selected == id);
	}

	/**
	 * Verificar usuario actualizado
	 */	
	$scope.isUpdated = function(id) {
		return ($scope.model.updated == id);
	}

	/**
	 * UserUpdatedEvent. Al actualizar un usuario:
	 *		Se modifica el usuario actualizado dentro de la lista de usuarios
	 *		Si no se encuentra el usuario actualizado, se listan nuevamente todos los usuarios
	 */
	$scope.$on('UserUpdatedEvent',function(event,id) {

		$scope.model.updated = id;

		var found = null;
		var pos = -1;

		// busco el usuario dentro de la lista de usuarios
		for (var i = 0; i < $scope.model.users.length; i++) {
		  var user = $scope.model.users[i];
		  if (user.id == id) {
			found = user;
			pos = i;
			break;
		  }
		}

		if (found == null) {
		  return;
		}

		// busco los datos del usuario actualizado, en caso de error busco nuevamente la lista.
		Users.findUser(found.id,

			function(user) {
				$scope.model.users[pos] = user;
			},

			function(error) {
			}
		);
	});
});
