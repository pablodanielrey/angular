
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
    rjSort: null,       //ordenamiento de la lista de justificaciones
    rjReversed: null   //flag para indicar el ordenamiento reverso de la lista de justificaciones

  };
  

  
  
  
  

  
  
  /**************************************
   * METODOS DE REQUESTED JUSTIFICACION *
   **************************************/
  $scope.loadRequestedJustifications = function() {
    Assistance.getJustificationRequestsToManage(['APPROVED'],"TREE",
      function(requestedJustifications) {
        $scope.model.requestedJustifications = requestedJustifications;
        if($scope.model.selectedUser !== null) $scope.filterUserRequestedJustifications();
      },
      function(error) {
        Notifications.message(error);
      }
    );
  };
  
   $scope.filterUserRequestedJustifications = function(){
    $scope.model.rjSort = ["dateSort", "justificationName"];
    $scope.model.rjReversed = false;
    $scope.model.requestedJustificationsFiltered = [];

    for (var i = 0; i < $scope.model.requestedJustifications.length; i++) {
      if(($scope.model.selectedUser.id === $scope.model.requestedJustifications[i].user_id) && ($scope.isAuthorizedJustification($scope.model.requestedJustifications[i].justification_id))){
        var req = Utils.formatRequestJustification($scope.model.requestedJustifications[i]);
        $scope.model.requestedJustificationsFiltered.push(req);
      }
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
      'e0dfcef6-98bb-4624-ae6c-960657a9a741',
      'b309ea53-217d-4d63-add5-80c47eb76820'
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

}]);
