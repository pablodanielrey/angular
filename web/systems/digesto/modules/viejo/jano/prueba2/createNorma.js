var app = angular.module('createNormaApp',[]);

app.controller('CreateNormaCtrl',
  function($scope) {

    $scope.apretasteElBoton = false;

    $scope.actionButton = function() {
      $scope.apretasteElBoton = !$scope.apretasteElBoton;

    }

    $scope.apretasteElBoton2 = false;
    $scope.actionButton2 = function() {
      $scope.apretasteElBoton2 = !$scope.apretasteElBoton2;

    }

  }
);
