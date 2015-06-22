
app.controller('ManageJustificationsStockCtrl', ["$scope", "$timeout", "$window", "Assistance", "Module", "Notifications", "Users",  "Utils", function($scope, $timeout, $window, Assistance, Module, Notifications, Users, Utils) {

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

    //seleccion de justificacion
    displayJustificationsList: false, //flag para controlar si se debe mostrar la lista de justificaciones
    selectedJustification: null,     //justificacion seleccionada
    searchJustification: null,       //justificacion buscada
    justifications: [],              //justificaciones consultadas para seleccionar
    justificationsSelectionDisable: true, //flag para indicar que se debe deshabilitar la seleccion
    
    stock: null,        //stock
    stockDisable: true, //flag para indicar que se debe deshabilitar el campo
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

    $scope.model.selectedJustification = null;
    $scope.model.searchJustification = null;
    $scope.model.displayJustificationsList = false;
    $scope.model.justificationsSelectionDisable = true;
    
    $scope.model.stock = null;
    $scope.model.stockDisable = true;
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
    $scope.loadJustifications();
  };
  
  
  /**************************************************************
   * METODOS CORRESPONDIENTES A LA SELECCION DE JUSTIFICACIONES *
   **************************************************************/
  /**
   * Cargar usuarios de la lista
   */
  $scope.loadJustifications = function(){        
    Assistance.getJustificationsByUser($scope.model.selectedUser.id,
      function(justifications) {
        $scope.model.justifications = justifications;
        $scope.model.usersSelectionDisable = false;
        $scope.model.justificationsSelectionDisable = false;
      },
      function(error){
        Notifications.message(error);
      }
    );
  };
  
  
  /**
   * Debe ser mostrada la lista de justificaciones?
   */
  $scope.isJustificationsListDisplayed = function() {
    return $scope.model.displayJustificationsList;

  };
  
  
  /**
   * Mostrar lista de justificaciones
   */
  $scope.displayJustificationsList = function(){
    $scope.model.selectedJustification = null;
    $scope.model.searchJustification = null;
    $scope.model.displayJustificationsList = true;
    $scope.model.justificationsSelectionDisable = false;
    
    $scope.model.stock = null;
    $scope.model.stockDisable = true;
  };
  
  /**
   * Esta seleccionado la justificacion?
   * @returns {Boolean}
   */
  $scope.isJustificationSelected = function(){
    return ($scope.model.selectedJustification !== null);
  };

  /**
   * Seleccionar justificacion
   * @param {justificacion} justificacion seleccionada
   */
  $scope.selectJustification = function(justification){
    $scope.model.displayJustificationsList = false;
    $scope.model.selectedJustification = justification;
    $scope.model.searchJustification = $scope.model.selectedJustification.name;
    $scope.model.stockDisable = false;
    $scope.loadStock();
  };
  
  
  
  /*****************************************************
   * METODOS CORRESPONDIENTES A LA DEFINICION DE STOCK *
   *****************************************************/
  $scope.loadStock = function(){
    $scope.model.stock = 10;
  };
  
}]);
