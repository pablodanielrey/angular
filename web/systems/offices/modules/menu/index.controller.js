(function() {
    'user strict'

    var app = angular.module('offices');
    app.controller('MenuCtrl', ['$scope','$location',

      function ($scope, $location) {
        $scope.selectOrders = function() {
          $location.path('/main');
        }

      }
    ]);

})();
