
app.controller('MyScheduleCtrl', ["$scope", "$window", "$timeout", "Assistance", "Notifications", "Session", "Users", function ($scope, $window, $timeout, Assistance, Notifications, Session, Users) { 
  
  //***** Definir variables *****
  if(!$scope.model) $scope.model = {};
  
  $scope.model.sessionUserId = null; //id de usuario conectado
  
  //variables del fieldset de horario semanal
  $scope.model.date = new Date();      //fecha seleccionada
  $scope.model.startHour = new Date(); //hora de inicio seleccionada
  $scope.model.sundayCheck = false;    //domingo
  $scope.model.mondayCheck = false;    //lunes
  $scope.model.tuesdayCheck = false;   //martes
  $scope.model.wednesdayCheck = false; //miercoles
  $scope.model.thursdayCheck = false;  //jueves
  $scope.model.fridayCheck = false;    //viernes
  $scope.model.saturdayCheck = false;  //sabado
  $scope.model.hours = 7;              //cantidad de horas seleccionadas

  //variables del fieldset de horario especial
  $scope.model.specialDate = new Date();      //fecha especial seleccionada
  $scope.model.startSpecialHour = new Date(); //hora de inicio especial
  $scope.model.specialHours = 7;              //cantidad de horas especiales
  
  //variables de seleccion de usuario
  $scope.model.searchUser = null;        //nombre del usuario a buscar
  $scope.model.searchUserPromise = null; //promesa de busqueda del usuario
  $scope.model.users = [];               //lista de usuarios consultados para los cuales el usuario logueado puede consultar
  $scope.model.displayListUser = false;  //flag para indicar si se debe visualizar la lista de usuarios consultados
  $scope.model.user = null;              //usuario seleccionado
  $scope.model.userSelected = false;     //flag para indicar que se ha seleccionado un usuario
   
  
  
  /*************************************
   * METODOS DE CARGA E INICIALIZACION *
   *************************************/
  $scope.initializeFieldsetNewSchedule = function(){
    //variables del fieldset de horario semanal
    $scope.model.date = new Date();      //fecha seleccionada
    $scope.model.startHour = new Date(); //hora de inicio seleccionada
    $scope.model.sundayCheck = false;    //domingo
    $scope.model.mondayCheck = false;    //lunes
    $scope.model.tuesdayCheck = false;   //martes
    $scope.model.wednesdayCheck = false; //miercoles
    $scope.model.thursdayCheck = false;  //jueves
    $scope.model.fridayCheck = false;    //viernes
    $scope.model.saturdayCheck = false;  //sabado
    $scope.model.hours = 7;              //cantidad de horas seleccionadas
  };
  
  $scope.initializeFieldsetNewSpecialSchedule = function(){
    $scope.model.specialDate = new Date();      //fecha especial seleccionada
    $scope.model.startSpecialHour = new Date(); //hora de inicio especial
    $scope.model.specialHours = 7;              //cantidad de horas especiales
  };
  
  
  /**
   * Cargar la programacion del usuario
   * @returns {undefined}
   */
  $scope.loadSchedule = function(){
    //TODO IMPLEMENTAR USO DE METODO
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
  
  
  $scope.loadScheduleTest = function(){
    var result = [
      {day:'monday', start:'10:00:00', end:'12:00:00'},
      {day:'monday', start:'15:00:00', end:'18:00:00'},
      {day:'tuesday', start:'09:00:00', end:'18:00:00'},
      {day:'wednesday', start:'15:00:00', end:'18:00:00'}
    ];
    
    $scope.setModelSchedule(result);
  };
  
  $scope.setModelSchedule = function(schedule){    
    $scope.model.schedule = {
      monday:[],
      tuesday:[],
      wednesday:[],
      thursday:[],
      friday:[],
      saturday:[],
      sunday:[]
    };
    
    for(var day in $scope.model.schedule){
      for(var i = 0; i < schedule.length; i++){
        if(day === schedule[i].day){
          var time = {start:schedule[i].start, end:schedule[i].end};
          $scope.model.schedule[day].push(time);
        }
      } 
    }
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
    $scope.loadUsers();
    $scope.loadScheduleTest();
    
  },0);
  
  
  
  
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
    $scope.model.userSelected = false;
    $scope.model.displayListUser = true;
  };
  
   /**
   * Esconder lista de usuarios
   */
  $scope.hideListUser = function(){
     $timeout(
      function(){
        $scope.model.displayListUser = false;
        if(!$scope.model.userSelected){
          if((!$scope.model.searchUser) || ($scope.model.searchUser === "")){
            $scope.model.user = null;
          } else if($scope.model.user){
            $scope.model.searchUser = $scope.model.user.name + " " + $scope.model.user.lastname;
          }
        }
      }
    ,100);
    
  };
  
  /**
   * Seleccionar usuario
   * @param {usuario} user Usuario seleccionado
   */
  $scope.selectUser = function(user){
    $scope.model.userSelected = true;
    $scope.model.user = user;
    $scope.model.searchUser = $scope.model.user.name + " " + $scope.model.user.lastname;
  };
  
  
  
}]);