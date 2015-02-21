
var app = angular.module('mainApp');

app.controller('EditUserProfileCtrl',function($scope,$rootScope,$timeout,Session) {

  $timeout(function() {
    var s = Session.getCurrentSession();
    if (s == null) {
      return;
    }

  	var uid = null;
  	if($rootScope.userId != null){
  		uid = $rootScope.userId;
  	} else {
  	    uid = s.user_id;
  	    s.selectedUser = s.user_id;
  	    Session.saveSession(s);

  	}

    $rootScope.$broadcast('UserSelectedEvent',uid);
  });

})
