var app = angular.module('createNormsApp',[]);

app.controller('createNormsCtrl', function($scope,$timeout) {

    $scope.model = {
      class:''
    }

    $scope.changeItem = function(item) {
      $scope.model.class = item;
    }


  }
);
