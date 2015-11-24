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

      var player = new Clappr.Player({source: "http://camaras.econo.unlp.edu.ar/c1/v.m3u8", parentId: "#player", width: "500", height: "300"});
      var player2 = new Clappr.Player({source: "http://camaras.econo.unlp.edu.ar/c2/v.m3u8", parentId: "#player2", width: "500", height: "300"});
      var player3 = new Clappr.Player({source: "http://camaras.econo.unlp.edu.ar/c3/v.m3u8", parentId: "#player3" , width: "500", height: "300"});
      var player4 = new Clappr.Player({source: "http://camaras.econo.unlp.edu.ar/c4/v.m3u8", parentId: "#player4" , width: "500", height: "300"});

    });



  }
);
