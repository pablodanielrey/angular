(function() {
    'user strict'

    var app = angular.module('assistance');
    app.controller('MenuCtrl', ['$scope','$location',

      function ($scope, $location) {
        $scope.selectOrders = function() {
          $location.path('/main');
        }
        $scope.selectReports = function() {
          $location.path('/reports');
        }

        $scope.selectSchedules = function() {
          $location.path("/schedules");
        }
      }
    ]);

})();
