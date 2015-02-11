var app = angular.module('mainApp');


/**
 * Controlador para editar el perfil del usuario
 * @service $scope
 * @service $log
 * @service Session
 * @service Utils
 * @service Users  
 *
 * @scope user
 * @scope clearUser()
 * @scope update()
 * @scope cancel() 
 *
 * @listen UserSelectedEvent
 * @listen UserUpdatedEvent
 */ 
app.controller('EditProfileCtrl', function($scope, $log, Session, Messages, Utils, Users) {

  $scope.user = {};

  $scope.clearUser = function() {
    $scope.user = { id:'', name:'', lastname:'', dni:'', telephone:'', genre:'', city:'', country:'', address:'', birthdate:'' }
  }

	$scope.$on('UserSelectedEvent', function(event,data) {
		$scope.clearUser();
	   
		Users.findUser(data,
			function(user) {
				user.birthdate = new Date(user.birthdate);
				$scope.user = user;
			},
			function(error) {
				alert(error);
			}
		);
	});

  $scope.$on('UserUpdatedEvent', function(event,data) {

    if ($scope.user.id != data) {
      // no es el usuario seleccionado, por lo que ignoro el evento ya que estoy mostrando otro usuario.
      return;
    }

    $scope.clearUser();
    Users.findUser(data,
      function(user) {
        user.birthdate = new Date(user.birthdate);
        $scope.user = user;
      },
      function(error) {
        alert(error);
      });
  });

	/**
	 * Actualizar usuario
	 */
	$scope.update = function() {
		if(($scope.user.birthdate != "") && ($scope.user.birthdate != null)){
			$scope.user.birthdate = new Date($scope.user.birthdate);	
		}

		Users.updateUser($scope.user,
			function(ok) {
				// nada
			},
			function(error) {
				alert(error);
			}
		);
	}

	/**
	 * Cancelar edicion de usuario
	 */
	$scope.cancel = function() {
		$scope.clearUser();
		if ($scope.user.id == undefined || $scope.user.id == null || $scope.user.id == '') {
		  return;
		}
		Users.findUser($scope.user.id,
		  function(user) {
			user.birthdate = new Date(user.birthdate);
			$scope.user = user;
		  },
		  function(error) {
			alert(error);
		  });
	}

  $scope.clearUser();

});
