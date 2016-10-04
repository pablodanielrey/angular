var app = angular.module('mainApp');

app.controller('MenuCtrl', ["$rootScope", '$scope','$location',

  function ($rootScope, $scope, $location) {

    $scope.selectEditAccount = function() {
      $location.path('/editAccounts');
    }

    $scope.selectCreateAccount = function() {
      $location.path('/createAccounts');
    }
  }
]);
