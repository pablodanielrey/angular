var app = angular.module('mainApp');

app.controller('UserAssistanceManagementCtrl', ["$scope", "$rootScope", "$timeout", "$window", "Session", "Assistance", "Profiles", "Notifications", "Utils", "Users", function($scope, $rootScope, $timeout, $window, Session, Assistance, Profiles, Notifications, Utils, Users) {

	$scope.model = {
    displayListUser: false, //flag para controlar si se debe mostrar la lista
    user: null, //usuario seleccionado
    searchUser: null, //usuario buscado
    users: [], //usuarios consultados para seleccionar
    
    //***** Cargar justificaciones para seleccion de secciones *****
    justifications: [],
    requestedJustifications: [], //se consultan todas las requestedJustifications aprobadas de todos los usuarios.
    userRequestedJustifications: [], //se filtran las requestedJustifications del usuario seleccionada y de las justificaciones que se pueden autorizar
    rjSort: null,
    rjReversed: false
	};

	
  
  
  /*************************************
   * METODOS DE CARGA E INICIALIZACION *
   *************************************/  
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
        if (ok !== 'granted') {
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
   * Cargar usuarios autorizados para aplicar justificaciones
   */
  $scope.loadAuthorizedUsers = function(){
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
  
  /**
   * Cargar justificaciones que puede autorizar el usuario
   */
  $scope.loadAuthorizedJustifications = function(){
    
    $scope.model.justifications = [
      {id:'478a2e35-51b8-427a-986e-591a9ee449d8', selected: false},
      {id:'f9baed8a-a803-4d7f-943e-35c436d5db46', selected: false},
      {id:'a93d3af3-4079-4e93-a891-91d5d3145155', selected: false},
      {id:'b80c8c0e-5311-4ad1-94a7-8d294888d770', selected: false},
      {id:'0cd276aa-6d6b-4752-abe5-9258dbfd6f09', selected: false}
    ];
    $scope.clearSelections();

  };
  
  /**
   * Verificar si la justificacion enviada como parametro es una justificacion autorizada
   * @param {type} justificationId Id de la justificacion
   * @returns {undefined}
   */
  $scope.isAuthorizedJustification = function(justificationId){
    for(var i = 0; i < $scope.model.justifications.length; i++){
      if($scope.model.justifications[i].id === justificationId) return true;
    }
    return false;
  };
  


  $scope.loadUserRequestedJustifications = function() {
    Assistance.getJustificationRequestsToManage(['APPROVED'],"TREE",
      function(requestedJustifications) {
        $scope.model.requestedJustifications = requestedJustifications;
        if($scope.model.user != null) $scope.filterUserRequestedJustifications();
      },
      function(error) {
        Notifications.message(error);
      }
    );
  };


  $scope.filterUserRequestedJustifications = function(){
    $scope.model.rjSort = ["dateSort", "justificationName"];
    $scope.model.rjReversed = false;
    $scope.model.userRequestedJustifications = [];
    for (var i = 0; i < $scope.model.requestedJustifications.length; i++) {
      if(($scope.model.user.id === $scope.model.requestedJustifications[i].user_id) && ($scope.isAuthorizedJustification($scope.model.requestedJustifications[i].justification_id))){
        var req = Utils.formatRequestJustification($scope.model.requestedJustifications[i]);
        $scope.model.userRequestedJustifications.push(req);
      }
    }
  };
    
  
  
  
  
  
  $scope.$on('JustificationsRequestsUpdatedEvent', function(event, requestUpdated) {
		if ($scope.model.user.id == requestUpdated.user_id) {
			$scope.loadUserRequestedJustifications();
     
		}
	});

	$scope.$on('JustificationStatusChangedEvent', function(event, requestChanged) {
		for (var i = 0; i < $scope.model.requestedJustifications.length; i++) {
			if ($scope.model.requestedJustifications[i].id == requestChanged.request_id) {
				$scope.loadUserRequestedJustifications();
				break;
			}
		}
	});
  
  
  
   /*********************************************
   * METODOS CORRESPONDIENTES A JUSTIFICACIONES *
   **********************************************/
  
  $scope.getJustificationIndex = function(justificationId){
    for(var i = 0; i < $scope.model.justifications.length; i++){
      if(justificationId === $scope.model.justifications[i].id){
        return i;
        break;
      }
    }
  };
  
  $scope.clearSelections = function() {
    for(var i = 0; i < $scope.model.justifications.length; i++){
      $scope.model.justifications[i].selected = false;
    }

	};
  
  
  $scope.cancelRequest = function(request) {
    Assistance.updateJustificationRequestStatus(request.id, status,
      function(ok) {
        console.log("ok")
      },
      function(error) {
        console.log("error");
      }
    );
  };
  
  $scope.sortRequestedJustifications = function(sort){
    if($scope.model.rjSort[0] === sort){
      $scope.model.rjReversed = !$scope.model.rjReversed;
    } else {
      switch($scope.model.rjSort[0]){
        case "dateSort":
          $scope.model.rjSort = ["dateSort", "justificationName"]
        break;
        case "justificationName":
          $scope.model.rjSort = ["justificationName", "dateSort"]
        break;
      }
      $scope.model.rjReversed = false;
    }
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
    $scope.model.userRequestedJustifications = [];
    $scope.model.displayListUser = true;
  };


  $scope.isSelectedUser = function(){
    return ($scope.model.user !== null);
  };
  

  /**
   * Seleccionar usuario
   * @param {usuario} user Usuario seleccionado
   */
  $scope.selectUser = function(user){
    $scope.model.displayListUser = false;
    $scope.model.user = user;
    $scope.model.searchUser = $scope.model.user.name + " " + $scope.model.user.lastname;
    $scope.filterUserRequestedJustifications();
  };








  $timeout(function() {
    $scope.loadSession();
    $scope.loadAuthorizedJustifications();
    $scope.loadAuthorizedUsers();
    $scope.loadUserRequestedJustifications()
  }, 0);

}]);
