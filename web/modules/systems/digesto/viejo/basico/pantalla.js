var app = angular.module('pantallaApp',[]);

app.controller('pantallaCtrl',function($scope) {

    /*
    $scope.click = false;

    $scope.actionButton = function() {
      $scope.click = !$scope.click;

    }
    */

    $scope.pantallaActual = -1;

    $scope.siguiente = function() {
      $scope.pantallaActual++;
    }

    $scope.volver = function() {
      if ($scope.pantallaActual >= 0) {
        $scope.pantallaActual--;
      }
    }

    $scope.finalizar = function() {
      $scope.pantallaActual = -1;
    }

  }
);
