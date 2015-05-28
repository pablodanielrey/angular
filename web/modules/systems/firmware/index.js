var app = angular.module('mainApp');

app.controller("IndexCtrl", ['$scope','$timeout','$location','Notifications', 'Firmware',function($scope, $timeout, $location, Notifications, Firmware) {

  $scope.model = {
    date:new Date(),
    day:'',
    hours:''
  }

  $scope.initialize = function() {
    $scope.updateDate();
    $scope.updateDay();
  }

  $scope.updateDay = function() {
    var options = {
        weekday: "long",
        year: "numeric",
        month: "2-digit",
        day: "numeric"
    };

    $scope.model.day = $scope.model.date.toLocaleDateString('es',options);
  }

  $scope.setHours = function() {
    var hs = ('0' + $scope.model.date.getHours()).slice(-2);
    var min = ('0' + $scope.model.date.getMinutes()).slice(-2);
    var sec = ('0' + $scope.model.date.getSeconds()).slice(-2);
    $scope.model.hours = hs + ":" + min + ":" + sec;
  }

  $scope.redirect = function() {
    $location.path('/enroll')
  }

  $scope.enterCode = function() {
    $scope.redirect();
  }

  $scope.updateDate = function() {
    var day = $scope.model.date.getDay();

    $scope.model.date = new Date();
    $scope.setHours();

    if (day != $scope.model.date.getDay()) {
        $scope.updateDay();
    }


    $timeout(function() {
      $scope.updateDate();
    }, 1000);
  }

  $scope.initialize();

}]);
