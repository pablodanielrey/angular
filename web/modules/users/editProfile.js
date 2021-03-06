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
app.controller('EditProfileCtrl', function($scope, $log, $timeout, Session, Messages, Utils, Users) {

  $scope.user = {};

  $scope.clearUser = function() {
    $scope.user = { id:'', name:'', lastname:'', dni:'', telephone:'', genre:'', city:'', country:'', address:'', birthdate:'', residenceCity:'', movil:'' }
  }

  /**
  * Carga los datos del usuario seleccionado dentro de la sesion, dentro de la pantalla de datos del perfil.
  */
  $scope.loadUserData = function() {
    var s = Session.getCurrentSession();
    if (s == null) {
      return;
    }
    if (s.selectedUser == undefined || s.selectedUser == null) {
      $scope.clearUser();
    }

    var uid = s.selectedUser;
    Users.findUser(uid,
      function(user) {
        user.birthdate = new Date(user.birthdate);
        $scope.user = user;
      },
      function(error) {
        //alert(error);
        $scope.clearUser();
      }
    );
  }


	$scope.$on('UserSelectedEvent', function(event,data) {
		$scope.clearUser();
    $scope.loadUserData();
/*
		Users.findUser(data,
			function(user) {
				user.birthdate = new Date(user.birthdate);
				$scope.user = user;
			},
			function(error) {
				//alert(error);
			}
		);
*/
	});

  $scope.$on('UserUpdatedEvent', function(event,data) {

    if ($scope.user.id != data) {
      // no es el usuario seleccionado, por lo que ignoro el evento ya que estoy mostrando otro usuario.
      return;
    }

    $scope.clearUser();
    $scope.loadUserData();
/*
    Users.findUser(data,
      function(user) {
        user.birthdate = new Date(user.birthdate);
        $scope.user = user;
      },
      function(error) {
        //alert(error);
      });
*/
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
				//alert(error);
			}
		);
	}

	/**
	* Cancelar edicion de usuario, se deben reinicializar los valores
	*/
	$scope.cancel = function() {
		$scope.clearUser();
		$scope.loadUserData();
	}

  $timeout(function() {
    $scope.clearUser();
    $scope.loadUserData();
  }, 0);

});
