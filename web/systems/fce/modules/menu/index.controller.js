var app = angular.module('mainApp');

app.controller('MenuCtrl', ["$rootScope", '$scope','$location',

  function ($rootScope, $scope, $location) {

    $scope.selectProfile = function() {
      $location.path('/profile');
    }

    $scope.selectPassword = function() {
      $location.path('/password');
    }

    $scope.selectMails = function() {
      $location.path('/mails');
    }

    $scope.selectSystems = function() {
      $location.path('/systems');
    }
  }
]);
