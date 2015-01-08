
var app = angular.module('mainApp');

app.controller('EditUserProfileCtrl',function($scope,$rootScope,$timeout,Session) {

  var s = Session.getCurrentSession();
  if (s == null) {
    return;
  }

  var uid = s.user_id;
  s.selectedUser = s.user_id;
  Session.saveSession(s);

  $rootScope.$broadcast('UserSelectedEvent',uid);

})
