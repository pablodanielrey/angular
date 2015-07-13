var app = angular.module('mainApp');

app.controller('createRegulation', function($scope,$timeout) {

    $scope.model = {
      class:'',
      contentFiltersView:false
    };


    $scope.changeItem = function(item) {
      $scope.model.class = item;
    }
    $scope.toggleFilters = function() {
      $scope.model.cerrado = !$scope.model.cerrado;
    }

    $scope.$on('$viewContentLoaded', function(event) {
      $scope.model.contentFiltersView = false;
    });

  }
);
