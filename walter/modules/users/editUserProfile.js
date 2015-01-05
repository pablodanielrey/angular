
var app = angular.module('mainApp');

app.controller('EditUserProfileCtrl',function($scope,$rootScope,$timeout,Session) {


  $timeout(function() {
    var s = Session.getCurrentSession();
    if (s == null) {
      return;
    }
    var uid = s.user_id;
    $rootScope.$broadcast('UserSelectedEvent',uid);
  }, 500);

})
