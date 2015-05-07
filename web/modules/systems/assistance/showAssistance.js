
var app = angular.module('mainApp');
app.controller('ShowAssistanceCtrl', ["$scope", "$timeout", "$window", "Notifications" , "Session", "Assistance", "Users", "Utils","$filter", function($scope, $timeout, $window, Notifications, Session, Assistance, Users, Utils,$filter) {






// Variables


  $scope.model = {

    base64:'',

    download:false,
    //datos de assistance correspondientes a los usuarios
    assistances: [],
      /*ejemplo: {user: null, //nombre de usuario
  	  start: null, //fecha y hora de inicio
	    end: null, //fecha y hora de finalizacion
	    logs: [], //logs
      justification: null,
	    workedTime: null,} //tiempo trabajado*/

	  start: new Date(), //fecha inicial de busqueda
    end: new Date(), //fecha final de busqueda

    groups: [],
    groupSelected:{},

    users: [], //usuarios consultados
    usersFilters:[], //usuarios fitlrados
    usersIdSelected: [], //ids de usuarios seleccionados
    searchUser: null, // string con el usuario buscado

  };

  $scope.disabled = false; //flag para deshabilitar busqueda


// ------------ ORDENACION ///////////////////
$scope.orderBy = $filter('orderBy');

$scope.order = function(predicate, reverse) {
  $scope.model.assistances = $scope.orderBy($scope.model.assistances, predicate, reverse);
};


// ----------- INICIALIZACION --------------------

  $scope.initialize = function() {
    $scope.loadSession();
    $scope.loadUsers();
    $scope.clearUsersSelected();
    $scope.model.download = false;

  }

  $scope.clearUsersSelected = function() {
    $scope.model.usersIdSelected = [];
  }

  $timeout(function() {
    $scope.initialize();
  },0);


  /**
   * Cargar y chequear session
   */
  $scope.loadSession = function(){
    if (!Session.isLogged()){
      Notifications.message("Error: Sesion no definida");
      $window.location.href = "/#/logout";
    } else {
      var session = Session.getCurrentSession();
      $scope.model.session_user_id = session.user_id;
    }
  };


  /**
    * Cargar usuarios
   */
  $scope.loadUsers = function() {
    $scope.model.users = [];
    $scope.model.usersFilters = [];

    Assistance.getUsersInOfficesByRole('autoriza',
      function(usersId) {
        if (usersId == null || usersId.length == 0) {
          usersId = [$scope.model.session_user_id];
        }

        $scope.loadGroups(usersId);
        $scope.defineUsers(usersId);
      },
      function(error){
        Notifications.message(error);
      }
    );
  };

  /**
   * Definir usuarios
   * @param usersId id de los usuarios a definir
   */
  $scope.defineUsers = function(usersId){
    for(var i = 0; i < usersId.length; i++){
      var id = usersId[i];
      Users.findUser(id,
        function(user){
          if(user != null) {
            $scope.model.users.push(user);
            $scope.model.usersFilters.push(user);
          }
        },
        function(error){
          Notifications.message(error);
        }
      );
    }
  };

  $scope.setParentGroup = function(group, groups) {
    for (var i = 0; i < groups.length; i++) {
      if (group.parent == groups[i].id) {
        group.parentName = groups[i].name;
        group.order = 1;
        return ;
      }
    }
    group.parentName = group.name;
    group.order = 0;
  }

  /**
    * Cargar todos los grupos
  */
  $scope.loadGroups = function(usersId) {
    $scope.model.groupSelected = {};
    $scope.model.groups = [];

    var userId = $scope.model.session_user_id;
    var tree = true;
    var role = 'autoriza';

    Assistance.getOfficesByUserRole(userId,role,tree,
      function(groups) {
        $scope.model.groups = groups;
        for (var i = 0; i < groups.length; i++) {
          $scope.setParentGroup(groups[i], groups);
        }
      },
      function(error) {
        Notifications.message(error);
      }
    );
  }


  $scope.include = function(users,uid) {
    for (var $i = 0; $i < users.length; $i++) {
      if (users[$i].id == uid) {
        return true;
      }
    }
    return false;
  }

  $scope.filterUsers = function() {
    $scope.model.usersFilters = $scope.model.users.slice();
    if ($scope.model.groupSelected == null) {
      return;
    }

    offices = [$scope.model.groupSelected.id];
    $scope.model.usersFilters = [];

    Assistance.getOfficesUsers(offices,
      function(users) {
        for (var $i = 0; $i < users.length; $i++) {
          var uid = users[$i];
          for (var $k = 0; $k < $scope.model.users.length; $k++) {
            var user = $scope.model.users[$k];
            if (uid == user.id && !$scope.include($scope.model.usersFilters,uid)) {
              $scope.model.usersFilters.push(user);
            }
          }
        }
      },
      function(error) {
        Notification.message(error);
      }
    );

  }

// ------------------------------------------------------------------------------------------------------------




  $scope.initializeSearchUsers = function(searchDates){

    var users = [];
    if (searchDates.length < 1) {
      return users;
    }

    if($scope.model.usersIdSelected.length == 0){
       users = $scope.model.usersFilters;
    } else {
       for(var i = 0; i < $scope.model.usersIdSelected.length; i++){
        var id = $scope.model.usersIdSelected[i];
        for(var j = 0; j < $scope.model.users.length; j++){
          var idAux = $scope.model.users[j].id;
          if(id == idAux){
            users.push($scope.model.users[j]);
            break;
          }
        }
      }
    }

    return users;
  };

  $scope.initializeSearchDates = function(){
    var dates = [];

    if($scope.model.start != null){
      if($scope.model.end != null){
        dates = Utils.getDates($scope.model.start, $scope.model.end);
      } else {
        dates.push($scope.model.start);
      }

    } else if($scope.model.end != null) {
      dates.push($scope.model.end);

    } else {
      dates.push(new Date());
    }

    return dates;

  };

  $scope.checkDates = function(){
    if($scope.model.start == null){
      $scope.model.start = new Date();
    }

    if(($scope.model.end === null) || ($scope.model.start > $scope.model.end)){
      $scope.model.end =  new Date($scope.model.start);
    }

    $scope.model.start.setHours(0,0,0,0);
    $scope.model.end.setHours(23,59,59,999);
  };

  $scope.getUsersIds = function(users) {
    var ids = [];
    for (var i = 0; i < users.length; i++) {
      ids.push(users[i].id);
    }
    return ids;
  }

  $scope.formatJustification = function(justification) {
    justification.startDate = Utils.formatDate(new Date(justification.begin));
    justification.startTime = Utils.formatTime(new Date(justification.begin));
    justification.endDate = Utils.formatDate(new Date(justification.end));
    justification.endTime = Utils.formatTime(new Date(justification.end));
  };



  /**
   * Metodo principal de busqueda de datos
   */
  $scope.searchAssistance = function(){
    if(!$scope.disabled) {
      $scope.checkDates();
      $scope.disabled = true; //deshabilitar nuevas busquedas hasta no completar la actual

      var status = "APPROVED"; //bsuca solo las justificaciones aprobadas

      $scope.model.assistances = [];
      $scope.searchDates = $scope.initializeSearchDates();

      if($scope.searchDates.length){
        var searchUsers = $scope.initializeSearchUsers($scope.searchDates); //si no existen usuarios seleccionados, se definen todos los usuarios

        $scope.usersIds = $scope.getUsersIds(searchUsers);
        Assistance.getAssistanceStatusByUsers($scope.usersIds, $scope.searchDates, status,
            function ok(response) {
              var assistances = response.assistances;
              $scope.model.base64 = response.base64;
              for (var i = 0; i < assistances.length; i++) {
                var assistance = assistances[i];
                var newAssistance = $scope.formatAssistance(assistance);
                if(assistance.userId != null){
                  if (assistance.justifications != null && assistance.justifications.length > 0) {
                    var j = assistance.justifications[0];
                    newAssistance.justification = Utils.getJustification(j.justification_id);
                    newAssistance.justification.begin = j.begin;
                    newAssistance.justification.end = j.end;
                    $scope.formatJustification(newAssistance.justification);
                    console.log(newAssistance.justification);
                  }
                  $scope.model.assistances.push(newAssistance);
                }

              }

              $scope.order('dateSort',false);//ordenamiento por defecto
              $scope.model.download = true;
              $scope.disabled = false;

            },
            function error(){
              // decremento el contador
              $scope.disabled = false;
              Notifications.message(error);
              throw new Error(error);
            }
          );
      }
    }
  };



  $scope.formatAssistance = function(assistance) {
    var newAssistance = {};

    newAssistance.displayLogs = false;
    newAssistance.displayJustification = false;

    var date = new Date(assistance.date);
    newAssistance.date = Utils.formatDate(date);

    newAssistance.dayOfWeek = {};
    newAssistance.dayOfWeek.name = Utils.getDayString(date);
    newAssistance.dayOfWeek.number = date.getDay();

    for(var i = 0; i < $scope.model.users.length; i++){
      var user = $scope.model.users[i];
      if(user.id == assistance.userId) {
        newAssistance.userId = assistance.userId;
        newAssistance.user = user.name + " " + user.lastname;
        break;
      }
    }

    newAssistance.dateSort = date;
    if(assistance.start != null){
      var start = new Date(assistance.start);
      newAssistance.dateSort = start;
      newAssistance.start = Utils.formatTime(start);
    };

    if(assistance.end != null){
      var end = new Date(assistance.end);
      newAssistance.end = Utils.formatTime(end);
    };

    newAssistance.logs = [];

    if (assistance.logs != null) {
      for(var i = 0; i < assistance.logs.length; i++){
        var date = new Date(assistance.logs[i]);
        var log = {};
        log.date = Utils.formatDate(date);
        log.time = Utils.formatTime(date);
        newAssistance.logs.push(log);
      }
    }

    if (assistance.workedMinutes != null) {
      newAssistance.workedTime = Utils.getTimeFromMinutes(assistance.workedMinutes);
    }

    if (assistance.status != null) {
      newAssistance.status = assistance.status;
    }

    return newAssistance;
  };


  /**
    * Seleccionar usuario
   */
  $scope.selectUser = function(user){
    var index = $scope.model.usersIdSelected.indexOf(user.id);
    if(index > -1){
      $scope.model.usersIdSelected.splice(index, 1);
    } else {
      $scope.model.usersIdSelected.push(user.id);
    }
  };

  $scope.isSelectedUser = function(user){
    var index = $scope.model.usersIdSelected.indexOf(user.id);
    if(index > -1){
      return true;
    } else {
      return false;
    }
  };

  $scope.showLogs = function(v,assistance) {
    assistance.displayLogs = v;
    assistance.displayJustification = false;
  };

  $scope.showJustifications = function(assistance) {
    assistance.displayLogs = false;
    assistance.displayJustification = !assistance.displayJustification;
  };

  $scope.isDisabled = function() {
    return ($scope.disabled) ;
  };



// ---------- EXPORTAR DATOS --------

  $scope.download = function() {
    if ($scope.model.base64 == null || $scope.model.base64 == '') {
      return;
    }
    var blob = Utils.base64ToBlob($scope.model.base64);
    window.saveAs(blob,'controlDeHorario.ods');
  }


}]);
