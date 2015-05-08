var app = angular.module('mainApp');

app.controller('UserAssistanceManagementCtrl', ["$scope", "$rootScope", "$timeout", "$window", "Session", "Assistance", "Profiles", "Notifications", "Utils", "Users", function($scope, $rootScope, $timeout, $window, Session, Assistance, Profiles, Notifications, Utils, Users) {

	$scope.model = {
    displayListUser: false, //flag para controlar si se debe mostrar la lista
    user: null, //usuario seleccionado
    searchUser: null, //usuario buscado
    users: [], //usuarios consultados para seleccionar
    
    //***** seleccion de modulos *****
		jmSelected: false,
    mcdSelected: false,
    mltSelected: false, 
    mafSelected: false,
    dSelected: false
	};

	
  $scope.clearSelections = function() {
		$scope.model.jmSelected = false;
    $scope.model.mcdSelected = false;
    $scope.model.mltSelected = false;
    $scope.model.mafSelected = false;
    $scope.model.dSelected = false;
	};
  
  
  /**
   * Cargar y chequear session
   */
  $scope.loadSession = function(){
    if (!Session.isLogged()){
      Notifications.message("Error: Sesion no definida");
      $window.location.href = "/#/logout";
    }
    $scope.model.sessionUserId = Session.getCurrentSessionUserId();
    if(!$scope.model.sessionUserId){
      Notifications.message("Error: No esta definido el usuario logueado");
      $window.location.href = "/#/logout";
    }
    Profiles.checkAccess(Session.getSessionId(),'ADMIN-ASSISTANCE,USER-ASSISTANCE',
      function(ok) {
        if (ok != 'granted') {
          Notifications.message("Acceso no autorizado");
          $window.location.href = "/#/logout";
        }
      },
      function (error) {
        Notifications.message(error);
      }
    );
  };
  
   /**
   * Cargar usuarios
   */
  $scope.loadUsers = function(){
    Assistance.getUsersInOfficesByRole('autoriza',
      function(users) {
        $scope.model.users = [];
        for (var i = 0; i < users.length; i++) {
          Users.findUser(users[i],
            function(user) {
              $scope.model.users.push(user);
            },
            function(error) {
              Notifications.message(error);
            });
        }
      },
      function(error){
        Notifications.message(error);
      }
    );
  };
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  /******************************************************
   * METODOS CORRESPONDIENTES A LA SELECCION DE USUARIO *
   ******************************************************/
  /**
   * Debe ser mostrada la lista de usuarios?
   */
  $scope.isDisplayListUser = function() {
    return $scope.model.displayListUser;

  };

  /**
   * Mostrar lista de usuarios
   */
  $scope.displayListUser = function(){
    $scope.model.user = null;
    $scope.model.searchUser = null;
    $scope.model.displayListUser = true;
  };

  

  /**
   * Seleccionar usuario
   * @param {usuario} user Usuario seleccionado
   */
  $scope.selectUser = function(user){
    $scope.model.displayListUser = false;
    $scope.model.user = user;
    $scope.model.searchUser = $scope.model.user.name + " " + $scope.model.user.lastname;
    //$scope.loadJustifications();

  };








  $timeout(function() {
    $scope.clearSelections();
    $scope.loadSession();
    $scope.loadUsers();
  }, 0);

}]);
