var app = angular.module('mainApp');

app.controller('HeaderCtrl', function($scope,$rootScope,$location) {

  $scope.goHome = function() {
    $location.path('/main');
    $rootScope.$broadcast("MenuOptionSelectedEvent",'Home');
  }

  $scope.logout = function() {
    $location.path('/logout');
    $rootScope.$broadcast("MenuOptionSelectedEvent",'Logout');
  }

});
