
app.controller('MyScheduleCtrl', ["$scope", "$window", "$timeout", "Assistance", "Notifications", "Session", "Users", "Utils", function ($scope, $window, $timeout, Assistance, Notifications, Session, Users, Utils) {

  /********************************
   * DEFINIR VARIABLES DEL MODELO *
   ********************************/
  if(!$scope.model) $scope.model = {};

  $scope.model.sessionUserId = null; //id de usuario conectado

  //variables del fieldset de horario semanal
  $scope.model.date = null;      //fecha seleccionada
  $scope.model.start = null; //hora de inicio seleccionada
  $scope.model.checkDay = {
    sunday:false,
    monday:false,
    tuesday:false,
    wednesday:false,
    thursday:false,
    friday:false,
    saturday:false
  };
  $scope.model.daySelected = null; //flag para indicar que se ha seleccionado al menos un dia
  $scope.model.end = null;              //horario de salida

  //variables del fieldset de horario especial
  $scope.model.specialDate = null;      //fecha especial seleccionada
  $scope.model.specialStart = null; //hora de inicio especial
  $scope.model.specialEnd = null;            //cantidad de horas especiales

  //variables de seleccion de usuario
  $scope.model.searchUser = null;        //nombre del usuario a buscar
  $scope.model.searchUserPromise = null; //promesa de busqueda del usuario
  $scope.model.users = [];               //lista de usuarios consultados para los cuales el usuario logueado puede consultar
  $scope.model.displayListUser = false;  //flag para indicar si se debe visualizar la lista de usuarios consultados
  $scope.model.user = null;              //usuario seleccionado



  /*************************************
   * METODOS DE CARGA E INICIALIZACION *
   *************************************/
  $scope.initializeFormNewSchedule = function(){
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

    $scope.model.start = null;

    $scope.model.end = null;

  };

  $scope.initializeFormNewSpecialSchedule = function(){
    $scope.model.specialDate = new Date();      //fecha especial seleccionada
    $scope.model.specialStart = null; //hora de inicio especial

    $scope.model.specialEnd = null;
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

    $scope.getDayOfWeek = function(date) {
      var weekday = ["sunday","monday","tuesday","wednesday","thursday","friday","saturday"]
      return weekday[date.getDay()];
    }

    Assistance.getSchedules($scope.model.user.id,
      function ok(response) {
        var schedules = response.schedule;
        var schedule = [];
        for (var $i = 0; $i < schedules.length; $i++) {
          var d = new Date(schedules[$i].start);
          var s = {};
          s.day = $scope.getDayOfWeek(d);
          s.start = schedules[$i].start;
          s.end = schedules[$i].end;
          schedule.push(s);
        }
        $scope.setModelSchedule(schedule);
      },
      function error(error) {
        Notifications.message(error);
      }

    )



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
    $scope.initializeFormNewSchedule();
    $scope.initializeFormNewSpecialSchedule();

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
    $scope.model.searchUser = null;
    $scope.model.displayListUser = true;
  };

  /**
   * Seleccionar usuario
   * @param {usuario} user Usuario seleccionado
   */
  $scope.selectUser = function(user){
    $scope.model.user = user;
    $scope.model.searchUser = $scope.model.user.name + " " + $scope.model.user.lastname;
    $scope.model.displayListUser = false;
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
   /*
   request:{
     user_id:"id del Usuario",
     date:"fecha de que se empieza a utilizar el schedule, si no se envia se toma la fecha actual",
     start:"hora de inicio del turno",
     end:"hora de fin de turno",
     daysOfWeek:[],
     isDayOfWeek:"es dia de la semana, si no se envia se toma como false",
     isDayOfMonth:"es dia un dia del mes, si no se envia se toma como false",
     isDayOfYear:"es dia del año, si no se envia se toma como false"
   }
   */

  $scope.getDaysOfWeek = function() {
    days = [];

    if ($scope.model.checkDay.sunday) {
      days.push("Sunday");
    }
    if ($scope.model.checkDay.monday) {
      days.push("Monday");
    }
    if ($scope.model.checkDay.tuesday) {
      days.push("Tuesday");
    }
    if ($scope.model.checkDay.wednesday) {
      days.push("Wednesday");
    }
    if ($scope.model.checkDay.thursday) {
      days.push("Thursday");
    }
    if ($scope.model.checkDay.friday) {
      days.push("Friday");
    }
    if ($scope.model.checkDay.saturday) {
      days.push("Saturday");
    }

    return days;
  }

  $scope.saveNewSchedule = function(){
    if(!$scope.isDaySelected()){
      return;
    }

    var request = {};
    request.user_id = $scope.model.user.id;
    request.date = $scope.model.date;
    request.start = $scope.model.start;
    request.end = $scope.model.end;
    request.daysOfWeek = $scope.getDaysOfWeek();
    request.isDayOfWeek = true;


    Assistance.newSchedule(request,
      function callbackOk(schedule){
        $scope.initializeFormNewSchedule();
        $scope.loadHistory();
        $scope.loadSchedule();
        Notifications.message("Horario almacenado con exito");
      },
      function callbackError(error){
        Notifications.message(error);
        throw new Error(error);
      }
    );


  };


  /*
  request:{
    user_id:"id del Usuario",
    date:"fecha de que se empieza a utilizar el schedule, si no se envia se toma la fecha actual",
    start:"hora de inicio del turno",
    end:"hora de fin de turno",
    daysOfWeek:[],
    isDayOfWeek:"es dia de la semana, si no se envia se toma como false",
    isDayOfMonth:"es dia un dia del mes, si no se envia se toma como false",
    isDayOfYear:"es dia del año, si no se envia se toma como false"
  }
  */
  $scope.saveNewSpecialSchedule = function() {

    var request = {};
    request.user_id = $scope.model.user.id;
    request.date = $scope.model.specialDate;
    request.start = $scope.model.specialStart;
    request.end = $scope.model.specialEnd;

    Assistance.newSchedule(request,
      function callbackOk(schedule){
        $scope.initializeFormNewSpecialSchedule();
        $scope.loadHistory();
        $scope.loadSchedule();
        Notifications.message("Horario especial almacenado con exito");
      },
      function callbackError(error){
        Notifications.message(error);
        throw new Error(error);
      }
    );
  };



}]);
