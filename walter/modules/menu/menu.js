
var app = angular.module('mainApp');

app.controller('MenuCtrl', function($rootScope, $scope, Session) {

  $scope.isMenuVisible = function() {
    return Session.isLogged();
  }

  $rootScope.$on('loginOk', function(event,data) {

  });

  $rootScope.$on('logoutOk', function(event,data) {

  });


});
