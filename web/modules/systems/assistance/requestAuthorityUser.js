
var app = angular.module('mainApp');

/**
 * Controlador utilizado para administrar la seleccion del usuario al cual se le quiere asignar horas extra
 */
app.controller('RequestAuthorityUserCtrl', ["$scope", "$timeout", "Assistance", "Notifications", "Users", function($scope, $timeout, Assistance, Notifications, Users) {

	if($scope.model == undefined){
		Notifications.message("Error: Variables del modelo sin definir");
	}

	$scope.model.searchUser = null; //usuario a buscar
	$scope.model.searchUserPromise = null //promesa de busqueda
	$scope.model.users = [] //lista de usuarios que coinciden con la busqueda
	
	
	/**
	 * Buscar usuarios
	 */
	$scope.searchUsers = function(){
		if($scope.model.searchUserPromise){
			$timeout.cancel($scope.model.searchUserPromise);
		}
		
		$scope.searchUserPromise = $timeout(
			function(){
				if($scope.search != "") {
					$scope.listUsers();
				}
			}
		,1000);
	};

	/**
 	 * Listar elementos
	 */
	$scope.selectUser = function(id){
		$scope.model.user_id = id;
	}
	
	/**
 	 * Seleccionar usuario
	 */
	$scope.listUsers = function(){
		Users.listUsers($scope.model.searchUser,
			function(users){
				$scope.model.users = users;
			},
			function(error){
				Notifications.message(error);
			}	
		)
	}
}]);
