(function() {
    'user strict'

    var app = angular.module('issues');
    app.controller('MenuCelCtrl', ['$scope','$location',
      function ($scope, $location) {

        $scope.selectHome = function() {
          $location.path('/home');
        }

        $scope.selectRequest = function() {
          $location.path('/request');
        }

      }
    ]);

})();
