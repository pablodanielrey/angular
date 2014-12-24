var app = angular.module('mainApp');

app.controller('MainCtrl', function($rootScope, $location, Session) {

  $rootScope.$on('loginOk',function(event,data) {
    $location.path('/main');
  });

  $rootScope.$on('logoutOk',function(event,data) {
    $location.path('/main');
  });


});
