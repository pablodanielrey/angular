(function() {
    'user strict'

    var app = angular.module('issues');
    app.controller('MenuCtrl', ['$scope','$location',

      function ($scope, $location) {
        $scope.selectOrders = function() {
          $location.path('/oders');
        }
        $scope.selectMyOrders = function() {
          $location.path('/myOrders');
        }

      }
    ]);

})();
