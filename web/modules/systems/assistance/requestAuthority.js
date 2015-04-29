
var app = angular.module('mainApp');

/**
 * Controlador utilizado para administrar "solicitudes de justificaciones" de una autoridad
 * A grandes rasgos podemos definir dos tipos de solicitudes de justificacion:
 *    Personal: Es la que realiza una persona para si mismo.
 *    Tercera: Es la que realiza una autoridad para un subordinado.
 * El objetivo del controlador es definir solicitudes a un subordinado. Actualmente la autoridad solo puede solicitar "horas extra"
 * El controlador debe identificar el usuario al cual se le va a definir la socicitud, el usuario es definido en otro controlador, se escucha el evento de seleccion de usuario
 */
app.controller('RequestAuthorityCtrl', ["$scope", "$timeout", "$window", "Assistance", "Notifications", "Users", "Session", "Utils", function($scope, $timeout, $window, Assistance, Notifications, Users, Session, Utils) {

  $scope.model = {
    session_user_id: null,        //id del usuario de session (correspondiente al jefe que solicita las horas extra)
    user_id: null,                //id del usuario para el cual se solicita la justificacion
    id: null,                     //id de la justificacion solicitada (actualmente solo se pueden solicitar horas extra que equivale a compensatorios)
    startTime: null,              //hora de inicio solicitada
    endTime: null,                //hora de finalizacion solicitada
    date: null,                   //actualmente se define un solo dia por solicitud, posteriormente cuando se maneje el calendario se podra definir un rango de dias (para un determinado rango de dias)
    reason: null,                 //motivo por el cual se solicita las horas extra
    requests: [],                 //solicitudes de horas extras para el usuario logueado
    sort: null,                   //ordenamiento de la lista de overtime
    reverse: false,               //definir ordenamiento en reversa de la lista de overtime

    //variables correspondientes a la seleccion de usuario
    searchUser: null,
    searchUserPromise: null,
    users: null,
    displayListUser: false
  };

  $scope.clearVars = function(){
    $scope.model.user_id = null;
    $scope.model.reason = null;
    $scope.model.searchUser = null;
    $scope.clearDate();
    $scope.clearStartTime();
    $scope.clearEndTime();
  };

  $scope.clearDate = function(){
    $scope.model.date = new Date();
    $scope.model.date.setSeconds(0);
    $scope.model.date.setMilliseconds(0);
  };

  $scope.clearStartTime = function(){
    $scope.model.startTime = new Date();
    $scope.model.startTime.setSeconds(0);
    $scope.model.startTime.setMilliseconds(0);
  };

  $scope.clearEndTime = function(){
    $scope.model.endTime = new Date();
    $scope.model.endTime.setSeconds(0);
    $scope.model.endTime.setMilliseconds(0);
  };

  $scope.checkDate = function(){
    if($scope.model.date === null){
      $scope.clearDate();
    }
  };

  $scope.checkStartTime = function(){
    if($scope.model.startTime === null){
      $scope.clearStartTime();
    }
    if($scope.model.startTime > $scope.model.endTime){
      $scope.model.endTime = $scope.model.startTime;
    }
  };

  $scope.checkEndTime = function(){
    if($scope.model.endTime === null){
      $scope.clearEndTime();
    }
    if($scope.model.startTime > $scope.model.endTime){
      $scope.model.endTime = $scope.model.startTime;
    }
  };


  /**
   * Cargar y chequear session
   */
  $scope.loadSession = function(){
    if (!Session.isLogged()){
      Notifications.message("Error: Sesion no definida");
      $window.location.href = "/#/logout";
    }
    var session = Session.getCurrentSession();
    $scope.model.session_user_id = session.user_id;
  };

  /**
   * Obtener solicitudes de horas extra del usuario (jefe)
   */
  $scope.loadRequests = function(){
    Assistance.getOvertimeRequests(null,
      function callbackOk(requests){
        $scope.model.requests = [];
        for(var i = 0; i < requests.length; i++){
          $scope.formatRequest(requests[i]);
        }
        $scope.sort = "dateSort";
      },
      function callbackError(error){
        Notifications.message(error);
        throw new Error(error);
      }
    );
  };

  /**
   * Dar formato a la solicitud de hora extra y almacenarla en el array $scope.model.requests
   */
  $scope.formatRequest = function(request) {
    var begin = new Date(request.begin);
    request.date = Utils.formatDate(begin);
    request.dateSort = Utils.formatDateExtend(begin);
    request.startTime = Utils.formatTime(begin);

    var end = new Date(request.end);
    request.endTime = Utils.formatTime(end);

    Users.findUser(request.user_id,
      function findUserCallbackOk(user) {
        request.user = user.name + " " + user.lastname;
        $scope.model.requests.push(request);
      },
      function findUserCallbackError(error) {
        Notifications.message(error);
        throw new Error(error);
      }
    );
  };


  $scope.$on('OvertimesUpdatedEvent',function(event, data) {
    console.log('OvertimesUpdatedEvent');
    $scope.loadRequests();
  });

  $scope.$on('OvertimeStatusChangedEvent',function(event, data) {
    console.log('OvertimeStatusChangedEvent');
    $scope.loadRequests();
  });


  /**
   * Inicializar
   */
  $timeout(function() {
    $scope.loadSession();
    $scope.loadRequests();
    $scope.clearVars();
  },0);




  /******************************************************
   * METODOS CORRESPONDIENTES A LA SELECCION DE USUARIO *
   ******************************************************/
  /**
   * Buscar usuarios
   */
  $scope.searchUsers = function(){
    $scope.model.displayListUser = true;
    if($scope.model.searchUserPromise){
      $timeout.cancel($scope.model.searchUserPromise);
    };

    $scope.model.searchUserPromise = $timeout(
      function(){
        $scope.listUsers();
      }
    ,1000);
  };


  $scope.isDisplayListUser = function() {
    return $scope.model.displayListUser;
  };

 /**
   * Esconder lista de usuarios
   */
  $scope.hideListUser = function(){
     $timeout(
      function(){
        $scope.model.displayListUser = false;
      }
    ,100);
  };

  /**
    * Listar elementos
   */
  $scope.selectUser = function(user){
    $scope.model.user_id = user.id;
    $scope.model.searchUser = user.name + " " + user.lastname;
  };

  /**
    * Seleccionar usuario
   */
  $scope.listUsers = function(){
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




  /***********************************************************
   * METODOS CORRESPONDIENTES AL PROCESAMIENTO DE FORMULARIO *
   ***********************************************************/



  /**
   * Guardar solicitud en el servidor
   */
  $scope.persistOvertime = function(){
    var begin = Utils.getTimestampFromDateAndTime($scope.model.date, $scope.model.startTime);
    var end = Utils.getTimestampFromDateAndTime($scope.model.date, $scope.model.endTime);

    var request = {
      date:$scope.model.date,
      begin:begin,
      end:end,
      reason:$scope.model.reason
    };

    Assistance.requestOvertime($scope.model.user_id, request,
      function callbackOk(response){
        $scope.clearVars();
      },
      function callbackError(error){
        Notifications.message(error);
      }
    );
  };

  /**
   * Chequear y guardar solicitud en el servidor
   */
  $scope.requestOvertime = function(){
    if(($scope.model.date != null) && ($scope.model.startTime != null) && ($scope.model.endTime != null) && ($scope.model.user_id != null) && ($scope.model.reason != null)) {
      $scope.persistOvertime();

    } else {
      Notifications.message("Datos incorrectos: Verifique los datos ingresados");
    }
  };


}]);
