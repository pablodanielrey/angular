var app = angular.module('mainApp');

app.controller('MenuCtrl', ["$rootScope", '$scope','$location',

  function ($rootScope, $scope, $location) {

    $scope.selectOrders = function() {

      $location.path('/libraty');
    }


  }
]);
