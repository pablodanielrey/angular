(function() {
    'user strict'

    var app = angular.module('assistance');
    app.controller('MenuCelCtrl', ['$scope','$location',
      function ($scope, $location) {

        $scope.selectOrders = function() {
          $location.path('/main');
        }

      }
    ]);

})();
