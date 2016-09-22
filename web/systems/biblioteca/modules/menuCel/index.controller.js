app.controller('MenuCelCtrl', ["$rootScope", '$scope','$location',

  function ($rootScope, $scope, $location) {

    $scope.selectOrders = function() {

      $location.path('/library');
    }

  }
]);
