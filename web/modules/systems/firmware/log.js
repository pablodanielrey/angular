var app = angular.module('mainApp');

app.controller("LogCtrl",["$rootScope","$scope","$timeout", "$location", function ($rootScope, $scope, $timeout, $location) {

  $scope.model = {
    user: {},
    date: new Date(),
    hours: ''
  }

  $scope.setDate = function() {
    var hs = ('0' + $scope.model.date.getHours()).slice(-2);
    var min = ('0' + $scope.model.date.getMinutes()).slice(-2);
    $scope.model.hours = hs + ":" + min;
  }

  $scope.initialize = function() {
      $scope.model.user = {}
      $scope.setDate();
      $timeout(function() {
        $location.path('/firmware');
      }, 5000);
  }

  $timeout(function() {
    $scope.initialize();
  },0);

  $rootScope.$on('logEvent', function(event, data) {
    console.log(data);
    console.log("logEvent");
    $scope.model.date = data.date;
    $scope.model.user = data.user;
  });

}]);
