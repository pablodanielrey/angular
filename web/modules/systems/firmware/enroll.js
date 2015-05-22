var app = angular.module('mainApp');

app.controller("EnrollCtrl", function($scope, $rootScope, $timeout, Session, Notifications) {


  $scope.model = {
    item:1,
    dni:null
  }

  $scope.next = function() {
    $scope.model.item = ($scope.model.item < 4) ? $scope.model.item+1 : 1;
  }

  $scope.cancel = function() {
    $scope.model.item = 1;
    $scope.model.dni = null;
  }

  $scope.save = function() {
    Notifications.message("Se ha enrolado correctamente al usuario " + $scope.model.dni);
  }

});
