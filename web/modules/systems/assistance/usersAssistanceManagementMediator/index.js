
app.controller('UsersAssistanceManagementMediatorCtrl', ["$scope", "$timeout", "Assistance", "Module", "Notifications", "Users",  "Utils", function($scope, $timeout, Assistance, Module, Notifications, Users, Utils) {

  /**
   * Variables del modelo en general
   */
  $scope.model = {
    sessionUserId: null, //id de sesion de usuario
    
    justificationsId: [],            //id de las justificaciones que el usuario tiene autorizadas
    justificationSelectedId: null,   //flag para indicar el id de la justificacion seleccionada si se debe mostrar la lista de usuarios
        
    //seleccion de usuario
    displayUserList: false,  //flag para controlar si se debe mostrar la lista de usuarios
    selectedUser: null,  //usuario seleccionado
    searchUser: null,  //usuario buscado
    users: [],        //usuarios consultados para seleccionar
    
    //requestedJustifications
    requestedJustifications: [],    //requerimientos del usuario seleccionado
    requestedJustificationsFiltered: null,   //requerimientos filtrados del usuario seleccionado
    rjSort: ["dateSort", "justificationName"],       //ordenamiento de la lista de justificaciones
    rjReversed: false,   //flag para indicar el ordenamiento reverso de la lista de justificaciones
    processingRequestedJustifications: false  //flag para indicar que se esta procesando

  };
  
  
  
  
  

  
  
  /**************************************
   * METODOS DE REQUESTED JUSTIFICACION *
   **************************************/
  $scope.loadRequestedJustifications = function() {
    $scope.model.processingRequestedJustifications = true;
    Assistance.getJustificationRequestsToManage(['APPROVED'],"TREE",
      function(requestedJustifications) {
        $scope.model.processingRequestedJustifications = false;
        $scope.model.requestedJustifications = requestedJustifications;
        if($scope.model.selectedUser !== null) $scope.filterUserRequestedJustifications();
      },
      function(error) {
        Notifications.message(error);
      }
    );
  };
  
   $scope.filterUserRequestedJustifications = function(){
   
    $scope.model.requestedJustificationsFiltered = [];

    for (var i = 0; i < $scope.model.requestedJustifications.length; i++) {
      if(($scope.model.selectedUser.id === $scope.model.requestedJustifications[i].user_id) && ($scope.isAuthorizedJustification($scope.model.requestedJustifications[i].justification_id))){
        var req = Utils.formatRequestJustification($scope.model.requestedJustifications[i]);
        $scope.model.requestedJustificationsFiltered.push(req);
      }
    }
  };
  
  
  $scope.cancelRequest = function(request) {
    $scope.model.processingRequestedJustifications = true;
    Assistance.updateJustificationRequestStatus(request.id, 'CANCELED',
      function(ok) {
        $scope.model.processingRequestedJustifications = false;
      },
      function(error) {
        $scope.model.processingRequestedJustifications = false;
        Notifications.message(error);
      }
    );
  };


  $scope.sortRequestedJustifications = function(sort){
    if($scope.model.rjSort[0] === sort){
      $scope.model.rjReversed = !$scope.model.rjReversed;
    } else {
      switch(sort){
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



  /****************************
   * METODOS DE JUSTIFICACION *
   ****************************/
  /**
   * Verificar si la justificacion enviada como parametro es una justificacion autorizada
   * @param {type} justificationId Id de la justificacion
   * @returns {undefined}
   */
  $scope.isAuthorizedJustification = function(justificationId){
    return ($scope.model.justificationsId.indexOf(justificationId) > -1);
  };
  
   /**
   * Cargar justificaciones que puede autorizar el usuario
   */
  $scope.loadAuthorizedJustifications = function(){
    
    $scope.model.justificationsId = [
      'e0dfcef6-98bb-4624-ae6c-960657a9a741', //AA
      '48773fd7-8502-4079-8ad5-963618abe725', //Comp
      'fa64fdbd-31b0-42ab-af83-818b3cbecf46', //BS
      '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb', //art 102
      'b70013e3-389a-46d4-8b98-8e4ab75335d0', //pre examen
      '76bc064a-e8bf-4aa3-9f51-a3c4483a729a', //licencia anual ordinaria
      '50998530-10dd-4d68-8b4a-a4b7a87f3972', //res 638
      //'f9baed8a-a803-4d7f-943e-35c436d5db46', //lm corta duracion
      //'a93d3af3-4079-4e93-a891-91d5d3145155', //lm lt
      //'b80c8c0e-5311-4ad1-94a7-8d294888d770', //lm af
      //'478a2e35-51b8-427a-986e-591a9ee449d8', //justificado medico
      //'5ec903fb-ddaf-4b6c-a2e8-929c77d8256f', //feriado
      //'874099dc-42a2-4941-a2e1-17398ba046fc', //paro
      'b309ea53-217d-4d63-add5-80c47eb76820', //cumple
      //'0cd276aa-6d6b-4752-abe5-9258dbfd6f09', //duelo
      //'e8019f0e-5a70-4ef3-922c-7c70c2ce0f8b' //donacion sangre
    ];

  };
  
  






  /******************************************************
   * METODOS CORRESPONDIENTES A LA SELECCION DE USUARIO *
   ******************************************************/
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
   * Debe ser mostrada la lista de usuarios?
   */
  $scope.isDisplayListUser = function() {
    return $scope.model.displayUserList;

  };

  /**
   * Mostrar lista de usuarios
   */
  $scope.displayListUser = function(){
    $scope.model.selectedUser = null;
    $scope.model.searchUser = null;
    $scope.model.displayUserList = true;

    $scope.model.requestedJustificationsFiltered = [];
  };

  /**
   * Esta seleccionado un usuario?
   * @returns {Boolean}
   */
  $scope.isSelectedUser = function(){
    return ($scope.model.selectedUser !== null);
  };
  

  /**
   * Seleccionar usuario
   * @param {usuario} user Usuario seleccionado
   */
  $scope.selectUser = function(user){
    $scope.model.displayUserList = false;
    $scope.model.selectedUser = user;
    $scope.model.searchUser = $scope.model.selectedUser.name + " " + $scope.model.selectedUser.lastname;
    $scope.filterUserRequestedJustifications();
  };
  
  
  
  
    
  /******************
   * INICIALIZACION *
   ******************/
  $scope.model.clearIndex = function(){
    $scope.model.displayUserList = false;
    $scope.model.selectedUser = null;
    $scope.model.searchUser = null;
    $scope.model.requestedJustificationsFiltered = [];
    $scope.model.rjSort = ["dateSort", "justificationName"];;
    $scope.model.rjReversed = false;
  };
  
  
  $timeout(function() {
    Module.authorize('ADMIN-ASSISTANCE,USER-ASSISTANCE');
    $scope.model.sessionUserId = Module.getSessionUserId();
    $scope.loadAuthorizedUsers();
    $scope.loadAuthorizedJustifications();
    $scope.loadRequestedJustifications();
    $scope.model.clearIndex();
  }, 0);
  
  
  $scope.$on('JustificationsRequestsUpdatedEvent', function(event, data){
    $scope.loadRequestedJustifications();

	});

	$scope.$on('JustificationStatusChangedEvent', function(event, data) {
    $scope.loadRequestedJustifications();
	});












}]);
