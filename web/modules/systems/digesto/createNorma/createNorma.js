var app = angular.module('createNormaApp',[]);

app.controller('CreateNormaCtrl',
  function($scope) {

    $scope.apretasteElBoton = false;

    $scope.actionButton = function() {
      $scope.apretasteElBoton = !$scope.apretasteElBoton;

    }

  

  }
);
