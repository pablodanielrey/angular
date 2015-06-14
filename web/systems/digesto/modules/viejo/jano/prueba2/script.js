var app = angular.module('miApp',[]);

app.controller('miCtrl', function($scope,$timeout) {

    $scope.model = {
      class:''
    }
    
    $scope.changeItem = function(item) {
      $scope.model.class = item;
    }


  }
);
