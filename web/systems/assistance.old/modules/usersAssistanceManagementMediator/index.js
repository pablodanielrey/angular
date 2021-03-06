
app.controller('UsersAssistanceManagementMediatorCtrl', ["$scope", "$wamp", "Session", "$timeout", "Assistance", "Office", "Module", "Notifications", "Users",  "Utils", function($scope, $wamp, Session, $timeout, Assistance, Office, Module, Notifications, Users, Utils) {

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
    Assistance.getJustificationRequestsToManage(['APPROVED','PENDING'],"TREE",
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
        Users.findUser(req.userId,
          function(user){
            req.userName = user.name + " " + user.lastname;
            Users.findUser(req.requestorId,
              function(user){
                req.requestorName = user.name + " " + user.lastname;
                $scope.model.requestedJustificationsFiltered.push(req);
              },
              function(error) {
                Notifications.message(error);
              }
            );
          },
          function(error) {
            Notifications.message(error);
          }
        );
      }
    }
  };


  $scope.approveRequest = function(request) {
    $scope.updateStatus("APPROVED",request);
  };

  $scope.refuseRequest = function(request) {
    $scope.updateStatus("REJECTED",request);
  };

  $scope.cancelRequest = function(request) {
    $scope.updateStatus("CANCELED",request);
  };



   $scope.updateStatus = function(status, request) {
        $scope.model.processingRequestedJustifications = true;

        Assistance.updateJustificationRequestStatus(request.id, status,
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
        case "userName":
          $scope.model.rjSort = ["userName", "justificationName", "dateSort"]
        break;
        case "requestorName":
          $scope.model.rjSort = ["requestorName", "justificationName", "dateSort"]
        break;
        case "dateSort":
          $scope.model.rjSort = ["dateSort", "justificationName", "dateSort"]
        break;
        case "justificationName":
          $scope.model.rjSort = ["justificationName", "dateSort"]
        break;
        case "status":
          $scope.model.rjSort = ["status", "justificationName", "dateSort"]
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
    $scope.model.justificationsId = []

    if($scope.model.selectedUser){
      Assistance.getJustificationsByUser($scope.model.selectedUser.id,
        function(justifications) {
          for (var i = 0; i < justifications.length; i++) {
            $scope.model.justificationsId.push(justifications[i].id);
            $scope.filterUserRequestedJustifications();
          }
        },
        function(error){
          Notifications.message(error);
        }
      );
    }

  };








  /******************************************************
   * METODOS CORRESPONDIENTES A LA SELECCION DE USUARIO *
   ******************************************************/
  /**
   * Cargar usuarios autorizados para aplicar justificaciones
   */
  $scope.loadAuthorizedUsers = function() {
    var sessionUserId = $scope.model.sessionUserId;
    Office.getUserInOfficesByRole(sessionUserId, 'autoriza', true,
      function(users) {
        $scope.model.users = [];

        // eliminamos el usuario jefe asi no se autoautoriza pedidos.
        var ind = users.indexOf($scope.model.sessionUserId)
        if (ind > -1) {
          users.splice(ind,1)
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
    $scope.loadAuthorizedJustifications();
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
    var s = Session.getCurrentSession();
    if ((!s) || (!s.user_id)) {
      Notifications.message("Error: Sesion no definida");
      $window.location.href = "/#/logout";
    } else {
        $scope.model.sessionUserId = Module.getSessionUserId();
        $wamp.subscribe('assistance.justification.JustificationsRequestsUpdatedEvent', JustificationsRequestsUpdatedEvent);
        $wamp.subscribe('assistance.justification.JustificationStatusChangedEvent', JustificationStatusChangedEvent);
        $scope.loadAuthorizedUsers();
        $scope.loadRequestedJustifications();
        $scope.model.clearIndex();
    }

  }, 0);


  function JustificationsRequestsUpdatedEvent(data) {
    $scope.$broadcast('JustificationsRequestsUpdatedEvent',data);
    $scope.loadRequestedJustifications();
  }

  function JustificationStatusChangedEvent(data) {
    $scope.$broadcast('JustificationStatusChangedEvent',data);
    $scope.loadRequestedJustifications();
  }

}]);
