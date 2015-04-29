
app.controller('MyScheduleCtrl', ["$scope", "$window", "$timeout", "Assistance", "Notifications", "Session", function ($scope, $window, $timeout, Assistance, Notifications, Session) { 
  
  //***** Definir variables *****
  if(!$scope.model) $scope.model = {};
  
  $scope.model.sessionUserId = null; //id de usuario conectado
  
  //variables del fieldset de horario semanal
  $scope.model.date = new Date(); //fecha seleccionada
  $scope.model.startHour = new Date(); //hora de inicio seleccionada
  $scope.model.sundayCheck = false;
  $scope.model.mondayCheck = false;
  $scope.model.tuesdayCheck = false;
  $scope.model.wednesdayCheck = false;
  $scope.model.thursdayCheck = false;
  $scope.model.fridayCheck = false;
  $scope.model.saturdayCheck = false; 
  $scope.model.hours = 7; //cantidad de horas seleccionadas

  //variables del fieldset de horario especial
  $scope.model.specialDate = new Date(); //fecha especial seleccionada
  $scope.model.startSpecialHour = new Date(); //hora de inicio especial
  $scope.model.specialHours = 7; //cantidad de horas especiales
  
  
  
  
  /*************************************
   * METODOS DE CARGA E INICIALIZACION *
   *************************************/
  /**
   * Cargar la programacion del usuario
   * @returns {undefined}
   */
  $scope.loadSchedule = function(){
    
    Assistance.getSchedule($scope.model.sessionUserId,
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
  };
  
  /**
   * Inicializar
   */
  $timeout(function() {
    $scope.loadSession();
    $scope.loadSchedule();
    
  },0);

  
}]);