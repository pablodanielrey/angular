var app = angular.module('createApp',[]);

app.controller('CreateCtrl',
  function($scope) {

    $scope.apretasteElBoton = false;

    $scope.actionButton = function() {
      $scope.apretasteElBoton = !$scope.apretasteElBoton;

    }

  }
);
