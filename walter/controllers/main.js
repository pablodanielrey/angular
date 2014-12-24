var app = angular.module('mainApp');

app.controller('MainCtrl', function($rootScope, $location, Session) {

  var sid = Session.getSessionId();
  if ((sid == undefined) || (sid == '') || (sid == null) || (sid == false)) {
    $location.path('/login');
  } else {
    $location.path('/main');
  }

  $rootScope.$on('loginOk',function(event,data) {
    $location.path('/main');
  });

  $rootScope.$on('logoutOk',function(event,data) {
    $location.path('/main');
  });


});
