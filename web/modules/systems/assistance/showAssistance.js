
var app = angular.module('mainApp'); 
app.controller('ShowAssistanceCtrl', ["$scope", "$timeout", "$window", "Notifications" , "Session", "Assistance", "Users", function($scope, $timeout, $window, Notifications, Session, Assistance, Users) {

  $scope.model = {
    //datos de assistance correspondientes a los usuarios
    assistances: [],
      /*ejemplo: {user: null, //nombre de usuario
  	  start: null, //fecha y hora de inicio
	    end: null, //fecha y hora de finalizacion
	    logs: [], //logs
	    workedTime: null,} //tiempo trabajado*/

	  
	  date: null, //fecha de busqueda
	  
	  session_user_id: null, //id del usuario de session
	  
    users: [],
    usersIdSelected: [],
    search: [] //almacena los usuarios que para los cuales actualmente se esta definiendo la asistencia

  }
  
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
  }
  
  /** 
    * Cargar usuarios 
   */   
  $scope.loadUsers = function(){
    Assistance.getUsersInOfficesByRole('autoriza', 
      function(usersId){
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
  
  
  $scope.initializeSearchAssistance = function(){
    var users = [];
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
    
    for(var i = 0; i < users.length; i++){
      var user = users[i];
      $scope.model.search.push(user.id);
    }
    
    
    return users;
  }
  
  $scope.searchAssistance = function(){
    if(!$scope.isSearch()){
      if($scope.model.date != null){
        $scope.model.assistances = [];
        var users = $scope.initializeSearchAssistance(); //si no existen usuarios seleccionados, se definen todos los usuarios
      
        for (var i = 0; i < users.length; i++){
          var user = users[i];          
        
          Assistance.getAssistanceStatusByDate(user.id, $scope.model.date,
            function ok(assistance){
              var newAssistance = $scope.formatAssistance(assistance, user.id);
              $scope.model.assistances.push(newAssistance);
         
              var index = $scope.model.search.indexOf(user.id);
              $scope.model.search.splice(index, 1);
            },
            function error(){
              Notifications.message(error);
              throw new Error(error);
            }
          );
        }
       } else {
        $scope.model.assistances = [];
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
      newAssistance.start = start.toLocaleTimeString();
    };
    
    if(assistance.end != null){
      var end = new Date(assistance.end);
      newAssistance.end = end.toLocaleTimeString();
    };
    
    newAssistance.logs = [];
   
    for(var i = 0; i < assistance.logs.length; i++){
      var log = new Date(assistance.logs[i]);
      newAssistance.logs.push(log.toLocaleTimeString());
    }
    
    var workedHours = Math.floor(assistance.workedMinutes / 60).toString();
    if(workedHours.length == 1) workedHours = "0" + workedHours;
    var workedMinutes = Math.round((assistance.workedMinutes % 60)).toString();
    if(workedMinutes.length == 1) workedMinutes = "0" + workedMinutes;
    newAssistance.workedTime = workedHours + ":" + workedMinutes;
    
    return newAssistance;
  }
  

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
  }
  
  $scope.isSearch = function(){
    return ($scope.model.search.length > 0);
  }
  
}]);

