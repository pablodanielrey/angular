
var app = angular.module('mainApp');
app.controller('ShowAssistanceCtrl', ["$scope", "$timeout", "$window", "Notifications" , "Session", "Assistance", "Users", "Utils", function($scope, $timeout, $window, Notifications, Session, Assistance, Users, Utils) {

  $scope.model = {
    //datos de assistance correspondientes a los usuarios
    assistances: [],
      /*ejemplo: {user: null, //nombre de usuario
  	  start: null, //fecha y hora de inicio
	    end: null, //fecha y hora de finalizacion
	    logs: [], //logs
	    workedTime: null,} //tiempo trabajado*/

	  start: null, //fecha inicial de busqueda
    end: null, //fecha final de busqueda

	  session_user_id: null, //id del usuario de session

    users: [], //usuarios consultados
    usersIdSelected: [], //ids de usuarios seleccionados
    searchUser: null, // string con el usuario buscado

    isSearch: [], //este array se utiliza para definir si se esta realizando una busqueda y en caso afirmativo deshabilitar una nueva busqueda. Los valores del array resultaran de una combinacion de los usuarios a buscar y las fechas a buscar. A medida que el servidor retorne datos para un usuario y fecha dadas, se iran eliminando los valores del array. CUando el array se encuentre vacio, significa que ya se realizaron todas las busquedas posibles.
  };

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
   * Definir usuarios
   * @param usersId id de los usuarios a definir
   */
  $scope.defineUsers = function(usersId){
    for(var i = 0; i < usersId.length; i++){
      var id = usersId[i];
      Users.findUser(id,
        function(user){
          if(user != null){
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
    * Cargar usuarios
   */
  $scope.loadUsers = function(){
    Assistance.getUsersInOfficesByRole('autoriza',
      function(usersId){
        if (usersId == null || usersId.length == 0) {
          usersId = [$scope.model.session_user_id];
        }
        console.log(usersId);
        $scope.defineUsers(usersId);
      },
      function(error){
        Notifications.message(error);
      }
    );
  };

  $timeout(function() {
    $scope.loadSession();
    $scope.loadUsers();
  },0);





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


  $scope.searchAssistance = function(){
    if(!$scope.isSearch()){
      $scope.model.assistances = [];
      var searchDates = $scope.initializeSearchDates();

      if(searchDates.length){
        var searchUsers = $scope.initializeSearchUsers(searchDates); //si no existen usuarios seleccionados, se definen todos los usuarios
        $scope.defineIsSearch(searchDates, searchUsers);
        for (var i = 0; i < searchDates.length; i++){
          for (var j = 0; j < searchUsers.length; j++){
            var date = searchDates[i];
            var user = searchUsers[j];
            Assistance.getAssistanceStatusByDate(user.id, date,
              function ok(assistance){
                var newAssistance = $scope.formatAssistance(assistance);
                $scope.removeIsSearchValue(assistance);
                if(assistance.start != null && assistance.userId != null){
                  $scope.model.assistances.push(newAssistance);
                }

              },
              function error(){
                Notifications.message(error);
                throw new Error(error);
              }
            );
          }
        }
      }
    }
  };



  $scope.formatAssistance = function(assistance) {
    var newAssistance = {};

    for(var i = 0; i < $scope.model.users.length; i++){
      var user = $scope.model.users[i];
      if(user.id == assistance.userId){
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

    for(var i = 0; i < assistance.logs.length; i++){
      var log = new Date(assistance.logs[i]);
      newAssistance.logs.push(Utils.formatTime(log));
    }

    newAssistance.workedTime = Utils.getTimeFromMinutes(assistance.workedMinutes);
    newAssistance.status = assistance.status;

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

  $scope.isSearch = function(){
    return ($scope.model.isSearch.length > 0);
  };

}]);
