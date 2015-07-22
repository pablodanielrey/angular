var app = angular.module('pruebaApp',[]);

app.controller('PruebaCtrl',
  function($scope) {

    $scope.apretasteElBoton = false;

    $scope.otro = function() {
      $scope.apretasteElBoton = !$scope.apretasteElBoton;
    }

  }
);
