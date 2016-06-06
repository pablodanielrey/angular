app.controller('MenuCelCtrl', ["$rootScope", '$scope','$location',

  function ($rootScope, $scope, $location) {

    $scope.selectHome = function() {

      $location.path('/home');
    }

    $scope.selectRequest = function() {
      $location.path('/request');
    }

    $scope.selectSchedule = function() {
      $location.path('/schedule');
    }
  }
]);
