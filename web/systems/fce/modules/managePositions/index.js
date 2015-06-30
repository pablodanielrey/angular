
app.controller('ManagePositionsCtrl', ["$scope", "$timeout", "$window", "Assistance", "Module", "Notifications", "Users",  "Utils", function($scope, $timeout, $window, Assistance, Module, Notifications, Users, Utils) {

   /**
   * Variables del modelo en general
   */
  $scope.model = {
    sessionUserId: null, //id de sesion de usuario

    //seleccion de usuario
    displayUsersList: false,  //flag para controlar si se debe mostrar la lista de usuarios
    selectedUser: null,  //usuario seleccionado
    searchUser: null,  //usuario buscado
    users: [],        //usuarios consultados para seleccionar
    usersSelectionDisable: true, //flag para indicar que se debe deshabilitar la seleccion

    //seleccion de cargo
    selectedPosition: null,     //justificacion seleccionada
    positions: [],              //justificaciones consultadas para seleccionar
    positionsSelectionDisable: true, //flag para indicar que se debe deshabilitar la seleccion
    
    submitButtonDisable: true
  };



  /******************
   * INICIALIZACION *
   ******************/
  $timeout(function() {
    Module.authorize('ADMIN-ASSISTANCE,USER-ASSISTANCE',
      function(response){
        if (response !== 'granted') {
          Notifications.message("Acceso no autorizado");
          $window.location.href = "/#/logout";
        }
        $scope.model.sessionUserId = Module.getSessionUserId();
        $scope.loadUsers();
        $scope.loadPositions();
      },
      function(error){
        Notifications.message(error);
        $window.location.href = "/#/logout";
      }
    );
  }, 0);



  /******************************************************
   * METODOS CORRESPONDIENTES A LA SELECCION DE USUARIO *
   ******************************************************/
  /**
   * Cargar usuarios de la lista
   */
  $scope.loadUsers = function(){
    Assistance.getUsersInOfficesByRole('autoriza',
      function(users) {
        $scope.model.users = [];

        // eliminamos el usuario jefe asi no se autoautoriza pedidos.
        var ind = users.indexOf($scope.model.sessionUserId);
        if (ind > -1) {
          users.splice(ind,1);
        }

        for (var i = 0; i < users.length; i++) {
          Users.findUser(users[i],
            function(user) {
              $scope.model.users.push(user);
            },
            function(error) {
              Notifications.message(error);
            });
        }
        
        $scope.model.usersSelectionDisable = false;
      },
      function(error){
        Notifications.message(error);
      }
    );
  };
  
  
  /**
   * Debe ser mostrada la lista de usuarios?
   */
  $scope.isUsersListDisplayed = function() {
    return $scope.model.displayUsersList;
  };
  
  
  /**
   * Mostrar lista de usuarios
   */
  $scope.displayUsersList = function(){
    $scope.model.selectedUser = null;
    $scope.model.searchUser = null;
    $scope.model.displayUsersList = true;
    $scope.model.usersSelectionDisable = false;

    $scope.model.selectedPosition = null;
    $scope.model.positionsSelectionDisable = true;
    $scope.model.submitButtonDisable = true;

  };
  
  /**
   * Esta seleccionado un usuario?
   * @returns {Boolean}
   */
  $scope.isUserSelected = function(){
    return ($scope.model.selectedUser !== null);
  };


  /**
   * Seleccionar usuario
   * @param {usuario} user Usuario seleccionado
   */
  $scope.selectUser = function(user){
    $scope.model.displayUsersList = false;
    $scope.model.selectedUser = user;
    $scope.model.searchUser = $scope.model.selectedUser.name + " " + $scope.model.selectedUser.lastname;
    $scope.model.usersSelectionDisable = true;
    
    $scope.loadUserPosition();
  };
  
  
  /**************************************************************
   * METODOS CORRESPONDIENTES A LA SELECCION DE JUSTIFICACIONES *
   **************************************************************/
  /**
   * Cargar posiciones
   */
  $scope.loadPositions = function(){
    $scope.model.positions= [
      "A2",
      "A3",
      "A4",
      "A5",
      "A6",
      "A7",
      "E2",
      "E3",
      "E4",
      "E5",
      "E6",
      "E7",
      "Contrato de Gestion",
      "Contrato de Obra",
      "Beca"
    ];
  };


  $scope.loadUserPosition = function(){
    Assistance.getPosition($scope.model.selectedUser.id,
      function(data){
          $scope.model.selectedPosition = data.position;
          $scope.model.positionsSelectionDisable = false;
      },
      function(error){
          Notifications.message(error);
      }
		);
    $scope.model.submitButtonDisable = false;
    $scope.model.usersSelectionDisable = false;
  };
  
  /**
   * Esta seleccionado la justificacion?
   * @returns {Boolean}
   */
  $scope.isPositionSelected = function(){
    return ($scope.model.selectedPosition !== null);
  };

 
  
  $scope.updateUserPosition = function(){
    Assistance.updatePosition($scope.model.selectedUser.id, $scope.model.selectedPosition,
				function(data){
            Notifications.message("Cargo Actualizado");
				},
				function(error){
						Notifications.message(error);
				}
		);
  }
  
}]);
