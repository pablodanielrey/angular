
var app = angular.module('mainApp'); 
app.controller('ShowAssistanceCtrl', ["$scope", "$timeout", "$window", "Notifications" , "Session", "Assistance", "Users", function($scope, $timeout, $window, Notifications, Session, Assistance, Users) {

  $scope.model = {
    //datos de assistance
	  start: null,
	  end: null,
	  logs: [],
	  workedTime: null,
	  
	  //fecha de busqueda
	  date: null,
	  
	  //id del usuario de session
	  session_user_id: null,
	  
	  //variables correspondientes a la seleccion de usuario
    users: null,
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
    * Cargar usuarios 
   */   
  $scope.loadUsers = function(){
    var callbackOk = function(users){
      $scope.model.users = users;
    }
    var callbackError = function(error){
      Notifications.message(error); 
    }
    Assistance.getUsersInOfficesByRole('autoriza', callbackOk, callbackError);
    //PRUEBA Users.listUsers("", callbackOk, callbackError);  
  };
  
  $timeout(function() { 
    $scope.loadSession();
    $scope.loadUsers();    
  },0);
  
  
  $scope.initializeAssistance = function(){
    $scope.model.start = null;
	  $scope.model.end = null;
	  $scope.model.logs = [];
	  $scope.model.workedTime = null;
  }
  
  
  $scope.searchAssistance = function(){
    if(($scope.model.date != null) && ($scope.model.selectedUserId != null)){
      Assistance.getAssistanceStatusByDate($scope.model.selectedUserId, $scope.model.date,
        function ok(assistance){
          $scope.initializeAssistance();
          /*PRUEBA var assistance = {
            start: '2015-01-01 10:00:00',
            end: '2015-01-01 18:00:00',            
            logs: [
              '2015-01-01 10:00:00',
              '2015-01-01 12:00:00',
              '2015-01-01 15:00:00',              
              '2015-01-01 18:00:00'
            ],
            workedMinutes: 1811,
          }*/
          
          $scope.formatAssistance(assistance);
        },
        function error(){
          Notifications.message(error);
          throw new Error(error);
        }
      );
    
    }
  }
  
  $scope.formatAssistance = function(assistance) {
    if(assistance.start != null){
      var start = new Date(assistance.start);
      $scope.model.start = start.toLocaleTimeString();
    };
    
    if(assistance.end != null){
      var end = new Date(assistance.end);
      $scope.model.end = end.toLocaleTimeString();
    };
    
    $scope.model.logs = [];
   
    for(var i = 0; i < assistance.logs.length; i++){
      var log = new Date(assistance.logs[i]);
      $scope.model.logs.push(log.toLocaleTimeString());
      
    }
    
    var workedHours = Math.floor(assistance.workedMinutes / 60).toString();
    if(workedHours.length == 1) workedHours = "0" + workedHours;
    var workedMinutes = (assistance.workedMinutes % 60).toString();
    if(workedMinutes.length == 1) workedMinutes = "0" + workedMinutes;
    $scope.model.workedTime = workedHours + ":" + workedMinutes;
  }
  

  /** 
    * Seleccionar usuario 
   */ 
  $scope.selectUser = function(user){ 
    $scope.model.selectedUserId = user.id;
    $scope.model.selectedUserName = user.name || " " || user.lastname;
    $scope.searchAssistance();
  }; 

  
}]);

