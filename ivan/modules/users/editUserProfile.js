
var app = angular.module('mainApp');

app.controller('EditUserProfileCtrl',function($scope,$routeParams,$rootScope,$timeout,Session) {

	if(($routeParams.userId == null) || ($routeParams.userId == undefined)){
		return;
	}

  $timeout(function() {
    var session = Session.getCurrentSession();
    if (session == null) {
      return;
    }


	var uid = null;
	
	if(session.selectedUser == null){
		session.selectedUser = session.user_id;
	    Session.saveSession(session);
	}

    $rootScope.$broadcast('UserSelectedEvent',$routeParams.userId);
  });
  
});