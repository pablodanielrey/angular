
app.controller('MyScheduleCtrl', ["$scope", "$window", "$timeout", "Assistance", "Notifications", "Session", "Users", "Utils", function ($scope, $window, $timeout, Assistance, Notifications, Session, Users, Utils) { 
  
  /********************************
   * DEFINIR VARIABLES DEL MODELO *
   ********************************/
  if(!$scope.model) $scope.model = {};
  
  $scope.model.sessionUserId = null; //id de usuario conectado
  
  //variables del fieldset de horario semanal
  $scope.model.date = null;      //fecha seleccionada
  $scope.model.hour = null; //hora de inicio seleccionada
  $scope.model.checkDay = {
    sunday:false,
    monday:false,
    tuesday:false,
    wednesday:false,
    thursday:false,
    friday:false,
    saturday:false
  };
  $scope.model.daySelected = null //flag para indicar que se ha seleccionado al menos un dia
  $scope.model.time = null;              //cantidad de horas seleccionadas

  //variables del fieldset de horario especial
  $scope.model.specialDate = null;      //fecha especial seleccionada
  $scope.model.specialHour = null; //hora de inicio especial
  $scope.model.specialTime = null;            //cantidad de horas especiales
  
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

    $scope.model.checkDay = {
      monday:true,
      tuesday:true,
      wednesday:true,
      thursday:true,
      friday:true,
      saturday:false,
      sunday:false
    };
        
    $scope.model.hour = null;
    
    $scope.model.time = new Date();
    $scope.model.time.setHours(7,0,0,0);

  };
  
  $scope.initializeFieldsetNewSpecialSchedule = function(){
    $scope.model.specialDate = new Date();      //fecha especial seleccionada
    $scope.model.specialHour = null; //hora de inicio especial
    
    $scope.model.specialTime = new Date();
    $scope.model.specialTime.setHours(7,0,0,0);
  };
  
  
  /**
   * Cargar la programacion del usuario
   * @returns {undefined}
   */
  $scope.loadSchedule = function(){
    /*TODO IMPLEMENTAR USO DE METODO
    Assistance.getSchedule($scope.model.user.id,
      function callbackOk(schedule){
        $scope.setModelSchedule(schedule);
      },
      function callbackError(error){
        Notifications.message(error);
        throw new Error(error);
      }
    );*/
    
    //DATOS DE PRUEBA, DEBEN SER BORRADOS AL IMPLEMENTAR EL METODO ANTERIOR
     var schedule = [
      {day:'monday', start:'2015-01-01 15:00:00', end:'2015-01-01 18:00:00'},
      {day:'wednesday', start:'2015-01-01 15:00:00', end:'2015-01-01 18:00:00'},
      {day:'monday', start:'2015-01-01 10:00:00', end:'2015-01-01 12:00:00'},
      {day:'thursday', start:'2015-01-01 18:00:00', end:null},
      {day:'friday', start:null, end:'2015-01-01 04:00:00'},
      {day:'tuesday', start:'2015-01-01 09:00:00', end:'2015-01-01 18:00:00'}
    ];
    
    $scope.setModelSchedule(schedule);
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
          if(schedule[i].start){
            var date = new Date(schedule[i].start);
            var time = {hour:Utils.formatTime(date), type:"start"};
            $scope.model.schedule[day].push(time);
          }
          if(schedule[i].end){
            var date = new Date(schedule[i].end);
            var time = {hour:Utils.formatTime(date), type:"end"};
            $scope.model.schedule[day].push(time);
          }
        }
      } 
    }
    
  };
  
  $scope.setModelHistory = function(history){       
  
  };



  $scope.loadHistory = function(){
   /*TODO IMPLEMENTAR USO DE METODO
    Assistance.getHistory($scope.model.user.id,
      function callbackOk(schedule){
        $scope.setModelHistory(history);
      },
      function callbackError(error){
        Notifications.message(error);
        throw new Error(error);
      }
    );*/
    
    //DATOS DE PRUEBA, DEBEN SER BORRADOS AL IMPLEMENTAR EL METODO ANTERIOR
     var history = [
      {date:'2015-01-01 15:00:00', description:'Nuevo horario semanal', start:'2015-01-01 18:00:00', end:'', days:''},
      {date:'2015-05-01 19:00:00', description:'Nuevo horario especial', start:'2015-01-01 18:00:00', end:'', days:null},
    ];
    
    $scope.setModelHistory(history);  
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
    $scope.initializeFieldsetNewSchedule();
    $scope.initializeFieldsetNewSpecialSchedule();
    
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
            $scope.model.schedule = []
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
    $scope.loadSchedule();
    $scope.loadHistory();

  };
  
  
  $scope.isDaySelected = function(){
    for(var day in $scope.model.checkDay){
      if($scope.model.checkDay[day]){
        return true;
      }
    }
    return false;
  };
  
  /*****************************
   * METODOS DE ADMINISTRACION *
   *****************************/
  $scope.saveNewSchedule = function(){
    if(!$scope.isDaySelected()){
      return;
    } 
    
    
    /*TODO IMPLEMENTAR USO DE METODO
    Assistance.saveNewSchedule($scope.model.user.id,
      function callbackOk(schedule){
        $scope.initializeFieldsetNewSchedule();
      },
      function callbackError(error){
        Notifications.message(error);
        throw new Error(error);
      }
    );*/
   
    $scope.initializeFieldsetNewSchedule();
    $scope.loadHistory();
    $scope.loadSchedule();
    Notifications.message("Horario almacenado con exito");

  };
  
  $scope.saveNewSpecialSchedule = function(){
     /*TODO IMPLEMENTAR USO DE METODO
    Assistance.saveNewSpecialSchedule($scope.model.user.id,
      function callbackOk(schedule){
        $scope.initializeFieldsetNewSpecialSchedule();
        $scope.loadHistory();  
      },
      function callbackError(error){
        Notifications.message(error);
        throw new Error(error);
      }
    )    $scope.initializeFieldsetNewSpecialSchedule();;*/
    $scope.initializeFieldsetNewSpecialSchedule();
    $scope.loadHistory();  
     $scope.loadSchedule();
    Notifications.message("Horario especial almacenado con exito");
  };
  
  
  
}]);