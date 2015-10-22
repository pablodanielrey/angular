
app.controller('MyScheduleCtrl', ["$scope", "$window", "$timeout", "Assistance", "Notifications", "Session", "Users", "Office", "Utils", function ($scope, $window, $timeout, Assistance, Notifications, Session, Users, Office, Utils) {

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

  $scope.getDayOfWeek = function(date) {
    var weekday = ["sunday","monday","tuesday","wednesday","thursday","friday","saturday"]
    return weekday[date.getDay()];
  }

  $scope.getDayOfWeekSpanish = function(date) {
    var weekday = ["Domingo","Lunes","Martes","Miércoles","Jueves","Viernes","Sábado"]
    return weekday[date.getDay()];
  }

  /**
   * Cargar la programacion del usuario
   * @returns {undefined}
   */
  $scope.loadSchedule = function(){
    Assistance.getSchedules($scope.model.user.id, $scope.model.dateOfWeek,
      function ok(schedules) {
        var schedule = [];
        for (var $i = 0; $i < schedules.length; $i++) {
          var sDay = schedules[$i];
          var d = new Date(sDay.start);
          var s = {};
          s.day = $scope.getDayOfWeek(d);
          s.start = sDay.start;
          schedule.push(s);

          var d = new Date(sDay.end);
          var s = {};
          s.day = $scope.getDayOfWeek(d);
          s.end = sDay.end;
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
            var time = {hour:Utils.formatTime(date), type:"start", date: date};
            $scope.model.schedule[day].push(time);
          }
          if(schedule[i].end){
            var date = new Date(schedule[i].end);
            var time = {hour:Utils.formatTime(date), type:"end", date: date};
            $scope.model.schedule[day].push(time);
          }
        }
      }
    }

  };


  $scope.loadHistory = function(){
    $scope.model.history = [];
    Assistance.getSchedulesHistory($scope.model.user.id,
      function ok(schedules) {
        var schedule = [];
        for (var $i = 0; $i < schedules.length; $i++) {

          var s = {};
          s.id = schedules[$i].id;
          s.start = new Date(schedules[$i].start);
          s.startDate =  Utils.formatDate(s.start);
          s.startTime = Utils.formatTime(s.start);
          s.day = $scope.getDayOfWeekSpanish(s.start);
          s.end = Utils.formatTime(new Date(schedules[$i].end));
          s.date = new Date(schedules[$i].date);
          s.dateStr = Utils.formatDate(s.date);
          s.isDayOfWeek = schedules[$i].isDayOfWeek;
          schedule.push(s);
        }

        $scope.model.history = schedule;
      },
      function error(error) {
        Notifications.message(error);
      }

    )

  };

  $scope.setProfileReadOnly = function() {

    $scope.model.readOnly = true;
    userId = $scope.model.sessionUserId;

    Users.findUser(userId,
      function(user) {
        $scope.model.users.push(user);
        $scope.selectUser(user);
      },
      function(error) {
        Notifications.message(error);
      });
  }

   /**
   * Cargar usuarios
   */
  $scope.loadUsers = function() {
    var userId = $scope.model.sessionUserId;
    var role = 'autoriza';
    var tree = true;
    Office.getUserInOfficesByRole(userId,role,tree,
      function(users) {
        $scope.model.users = [];

        if (users == null || users.length <= 0) {
          $scope.setProfileReadOnly();
          return;
        }

        $scope.model.readOnly = false;
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
  $scope.loadSession = function() {
    var s = Session.getCurrentSession();
		if ((!s) || (!s.user_id)) {
      Notifications.message("Error: Sesion no definida");
      $window.location.href = "/#/logout";
    } else {
      var session = Session.getCurrentSession();
      $scope.model.sessionUserId = session.user_id;
    }
  };

  /**
   * Inicializar
   */
  $timeout(function() {

    $scope.model.dateOfWeek = new Date();
    $scope.model.readOnly = true;

    $scope.loadSession();
    $scope.loadUsers();
    $scope.initializeFormNewSchedule();
    $scope.initializeFormNewSpecialSchedule();

  },0);

  $scope.getFirstWeekDay = function(date) {
    var day = date.getDay();
    //el getDay comienza con Dom, le resto uno para que empiece desde el lunes
    day = (day == 0) ? day = 6 : day = day - 1;
    date = new Date(date.getTime() - (day*24*60*60*1000));
    return date;
  }

  $scope.setWeekStr = function() {
    var firstDate = $scope.getFirstWeekDay($scope.model.dateOfWeek);
    var endDate = new Date(firstDate.getTime() + (6*24*60*60*1000));
    $scope.model.dateOfWeekStr = Utils.formatDate(firstDate) + ' - ' + Utils.formatDate(endDate);
  }

  $scope.$watch('model.dateOfWeek', function(newValue, oldValue) {
    if (newValue == null) {
      $scope.model.dateOfWeek = oldValue;
      return;
    }
    $scope.setWeekStr();
    if ($scope.model.user != null) {
      $scope.loadSchedule();
    }
  });




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
    if ($scope.model.readOnly) {
      return;
    }
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
    if(!$scope.isDaySelected() || $scope.model.readOnly){
      return;
    }

    var request = {};
    request.user_id = $scope.model.user.id;
    request.date = $scope.model.date;

    var s = $scope.model.start;
    request.start = s.getHours() * 60 * 60 + s.getMinutes() * 60 + s.getSeconds();

    var e = $scope.model.end;
    request.end = e.getHours() * 60 * 60 + e.getMinutes() * 60 + e.getSeconds();

    request.daysOfWeek = $scope.getDaysOfWeek();


    Assistance.persistScheduleWeek(request,
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

    if ($scope.model.readOnly) {
      return;
    }

    var request = {};
    request.user_id = $scope.model.user.id;
    request.date = $scope.model.specialDate;

    var s = $scope.model.specialStart;
    request.start = s.getHours() * 60 * 60 + s.getMinutes() * 60 + s.getSeconds();

    var e = $scope.model.specialEnd;
    request.end = e.getHours() * 60 * 60 + e.getMinutes() * 60 + e.getSeconds();

    Assistance.persistSchedule(request,
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


  $scope.delete = function(id) {
    if ($scope.model.readOnly) {
      return;
    }
    Assistance.deleteSchedule(id,
      function callbackOk(ok) {
        $scope.loadHistory();
        $scope.loadSchedule();
        Notifications.message("Se ha eliminado correctamente")
      },
      function callbackError(error){
        Notifications.message(error);
      }
    );
  }

}]);
