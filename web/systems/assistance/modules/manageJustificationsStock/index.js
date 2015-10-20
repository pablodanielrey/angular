
app.controller('ManageJustificationsStockCtrl', ["$scope", "$timeout", "$window", "Assistance", "Office",  "Notifications", "Users",  "Utils", function($scope, $timeout, $window, Assistance, Office, Notifications, Users, Utils) {

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
    
    submitButtonDisable: true
  };



  /******************
   * INICIALIZACION *
   ******************/
  $timeout(function() {
    $scope.loadUsers();
  }, 0);



  /******************************************************
   * METODOS CORRESPONDIENTES A LA SELECCION DE USUARIO *
   ******************************************************/
  /**
   * Cargar usuarios de la lista
   */
  $scope.loadUsers = function(){
    Office.getUserInOfficesByRole('autoriza',
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
    $scope.displayJustificationsList();
  };
  
  
  /**************************************************************
   * METODOS CORRESPONDIENTES A LA SELECCION DE JUSTIFICACIONES *
   **************************************************************/
  /**
   * Cargar usuarios de la lista
   */
  $scope.loadJustifications = function(){
    $scope.model.justifications = [];
    $scope.model.selectedJustification = null;
    
    Assistance.getJustificationsByUser($scope.model.selectedUser.id,
      function(justifications) {
        /** filtrar las justificaciones para incluir solo aquellas a las que se puede editar el stock **/
        for(var i = 0; i < justifications.length; i++){
          switch(justifications[i].id){
            /**
             * AGREGAR ACA LAS JUSTIFICACIONES QUE SE PUEDE CAMBIAR EL STOCK.
             */
            case "48773fd7-8502-4079-8ad5-963618abe725": //compensatorio
            case "b70013e3-389a-46d4-8b98-8e4ab75335d0": //pre examen
            case "50998530-10dd-4d68-8b4a-a4b7a87f3972": //res 638
            case "76bc064a-e8bf-4aa3-9f51-a3c4483a729a": //licencia anual ordinaria
              $scope.model.justifications.push(justifications[i]);
            break;
            
          }
        
        }

        $scope.model.usersSelectionDisable = false;
  
        if($scope.model.justifications.length <= 0){
          $scope.model.justificationsSelectionDisable = true;
          $scope.model.searchJustification = "No existen justificaciones";

        }
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
    $scope.model.submitButtonDisable = true;
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
   * @param {justificacion} justification seleccionada
   */
  $scope.selectJustification = function(justification){
    $scope.model.displayJustificationsList = false;
    $scope.model.selectedJustification = justification;
    $scope.model.searchJustification = $scope.model.selectedJustification.name;
    $scope.loadStock();
  };
  
  
  $scope.checkStock = function(){
    if($scope.model.stock < 0){
      $scope.model.stock = 0;
    }
  }
  
  
  /*****************************************************
   * METODOS CORRESPONDIENTES A LA DEFINICION DE STOCK *
   *****************************************************/
  $scope.loadStock = function(){
    $scope.model.submitButtonDisable = true;
    $scope.model.stockDisable = true;

    Assistance.getJustificationStock($scope.model.selectedUser.id, $scope.model.selectedJustification.id, null, null,
				function(data){
            $scope.model.stock = data.stock;
            $scope.model.submitButtonDisable = false;
            $scope.model.stockDisable = false;
				},
				function(error){
						Notifications.message(error);
				}
		);
    
  };
  
  
  $scope.updateJustificationStock = function(){
    Assistance.updateJustificationStock($scope.model.selectedUser.id, $scope.model.selectedJustification.id, $scope.model.stock,
				function(data){
            Notifications.message("Stock Actualizado");
				},
				function(error){
						Notifications.message(error);
				}
		);
  }
  
}]);
