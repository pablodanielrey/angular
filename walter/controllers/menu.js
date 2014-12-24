
var app = angular.module('mainApp');

app.controller('MenuCtrl', function($rootScope, $scope, Session) {

  $rootScope.$on('loginOk', function(event,data) {
    $scope.menuDisplay = 'inline';
  });

  $rootScope.$on('logoutOk', function(event,data) {
    $scope.menuDisplay = 'none';
  });

  $scope.menuDisplay = 'none';

});
