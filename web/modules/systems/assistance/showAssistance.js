
var app = angular.module('mainApp');
app.controller('ShowAssistanceCtrl', ["$scope", "$timeout", "$window", "Notifications" , "Session", "Assistance", "Users", "Utils", function($scope, $timeout, $window, Notifications, Session, Assistance, Users, Utils) {


// Variables

  $scope.model = {
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

    isSearch: [], //este array se utiliza para definir si se esta realizando una busqueda y en caso afirmativo deshabilitar una nueva busqueda. Los valores del array resultaran de una combinacion de los usuarios a buscar y las fechas a buscar. A medida que el servidor retorne datos para un usuario y fecha dadas, se iran eliminando los valores del array. CUando el array se encuentre vacio, significa que ya se realizaron todas las busquedas posibles.
  };

  $scope.count = 0;
  $scope.disabled = false;


// ----------- INICIALIZACION --------------------

  $scope.initialize = function() {
    $scope.loadSession();
    $scope.loadUsers();
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
          }
        },
        function(error){
          Notifications.message(error);
        }
      );
    }
  };

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
        console.log(groups);
      },
      function(error) {
        Notifications.message(error);
      }
    );
  }

  $scope.$watch('model.groupSelected', $scope.filterUsers);

  $scope.filterUsers = function() {
    $scope.model.usersFilters = $scope.model.users.slice();
    if ($scope.model.groupSelected == null) {
      return;
    }



  }

// ------------------------------------------------------------------------------------------------------------




  $scope.initializeSearchUsers = function(searchDates){

    var users = [];
    if (searchDates.length < 1){
      return users;
    }

    if($scope.model.usersIdSelected.length == 0){
       users = $scope.model.users;
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


  $scope.defineIsSearch = function(searchDates, searchUsers){
    for(var i = 0; i < searchDates.length; i++){
      for(var j = 0; j < searchUsers.length; j++){
        var strDate = searchDates[i].toLocaleDateString();
        var strUserId = searchUsers[j].id;
        $scope.model.isSearch.push(strDate + strUserId);
      }
    }
  };

  $scope.removeIsSearchValue = function(assistance){
    if(assistance.start == null || assistance.userId == null || $scope.model.isSearch.length === 0){
      $scope.model.isSearch = [];
      return;
    }

    var start = new Date(assistance.start);
    var userId = assistance.userId;

    var isSearch = start.toLocaleDateString()+userId;
    var index = $scope.model.isSearch.indexOf(isSearch);
    $scope.model.isSearch.splice(index, 1);
  };

  $scope.getUsersIds = function(users) {
    var ids = [];
    for (var i = 0; i < users.length; i++) {
      ids.push(users[i].id);
    }
    return ids;
  }

  $scope.formatJustification = function(justification) {
    justification.startDate = Utils.formatTime(new Date(justification.begin));
    justification.startTime = Utils.formatTime(new Date(justification.begin));
    justification.endDate = Utils.formatDate(new Date(justification.end));
    justification.endTime = Utils.formatTime(new Date(justification.end));
  }

  $scope.setJustifications = function(justifications) {

    // tiene las justificaciones que no machean con ninguna asistencia
    var auxJustifications = justifications.slice();
    for (var $i = 0; $i < justifications.length; $i++) {
      var j = justifications[$i];
      j.date = new Date(j.begin);
      j.date = Utils.formatDate(j.date);
      for (var $k = 0; $k < $scope.model.assistances.length; $k++) {
        var a = $scope.model.assistances[$k];
        if (j != null && a.date == j.date) {
          var index = auxJustifications.indexOf(j);
          auxJustifications.splice(index,1);
          a.justification = j;
          $scope.formatJustification(a.justification);
        }
      }
    }

    for (var $i = 0; $i < auxJustifications.length; $i++) {
      var j = auxJustifications[$i];
      var newAssistance = {};
      newAssistance.userId = j.user_id;
      newAssistance = $scope.formatAssistance(newAssistance);
      newAssistance.date = Utils.formatDate(new Date(j.begin));
      newAssistance.dateSort = Utils.formatDateExtend(new Date(j.begin));
      newAssistance.displayLogs = false;
      newAssistance.displayJustification = false;

      newAssistance.justification = j;
      $scope.formatJustification(j);
      $scope.model.assistances.push(newAssistance);
    }


    // decremento el contador
    $scope.count = 0;
    $scope.disabled = false;
  }

  $scope.getJustifications = function() {
    // requestJustification buscar la justificacion
    var status = null;
    var start = $scope.model.start;
    var end = $scope.model.end;
    Assistance.getJustificationRequestsByDate(status, $scope.usersIds, start, end,
      function ok(requests) {
        $scope.setJustifications(requests);
      },
      function error() {
        // decremento el contador
        $scope.count = 0;
        $scope.disabled = false;
      }
    );
  }

  $scope.searchAssistance = function(){
    if(!$scope.disabled) {

      $scope.predicate = 'dateSort';

      $scope.model.assistances = [];
      $scope.searchDates = $scope.initializeSearchDates();

      if($scope.searchDates.length){
        var searchUsers = $scope.initializeSearchUsers($scope.searchDates); //si no existen usuarios seleccionados, se definen todos los usuarios
        $scope.defineIsSearch($scope.searchDates, searchUsers);

        // cantidad de elementos a buscar, es para deshabilitar el buscador
        $scope.count = $scope.searchDates.length * searchUsers.length;
        $scope.disabled = true;

        $scope.usersIds = $scope.getUsersIds(searchUsers);
        Assistance.getAssistanceStatusByUsers($scope.usersIds, $scope.searchDates,
            function ok(assistances) {

              for (var i = 0; i < assistances.length; i++) {
                var assistance = assistances[i];
                var newAssistance = $scope.formatAssistance(assistance);
                newAssistance.displayLogs = false;
                newAssistance.displayJustification = false;
                if(assistance.start != null && assistance.userId != null){
                  $scope.model.assistances.push(newAssistance);
                }

              }

              $scope.getJustifications();

            },
            function error(){
              // decremento el contador
              $scope.count = 0;
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

    for(var i = 0; i < $scope.model.users.length; i++){
      var user = $scope.model.users[i];
      if(user.id == assistance.userId) {
        newAssistance.userId = assistance.userId;
        newAssistance.user = user.name + " " + user.lastname;
        break;
      }
    }

    if(assistance.start != null){
      var start = new Date(assistance.start);
      newAssistance.date = Utils.formatDate(start);
      newAssistance.dateSort = Utils.formatDateExtend(start);
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

  $scope.resetSearchUser = function(){
    $scope.model.usersIdSelected = [];
  }

  $scope.showLogs = function(v,assistance) {
    assistance.displayLogs = v;
    assistance.displayJustification = v;
  }

  $scope.showJustifications = function(assistance) {
    assistance.displayJustification = !assistance.displayJustification;
  }

  $scope.isDisabled = function() {
    return ($scope.disabled) || ($scope.model.start == null) || ($scope.model.end == null);
  }


}]);
