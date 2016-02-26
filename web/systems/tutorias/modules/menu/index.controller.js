var app = angular.module('mainApp');

app.controller('MenuCtrl', ["$rootScope", '$scope','$location',

  function ($rootScope, $scope, $location) {

    $scope.selectCreateTutoring = function() {
      $location.path('/createTutoring');
    }

    $scope.selectMyTutorings = function() {
      $location.path('/myTutorings');
    }
  }
]);
