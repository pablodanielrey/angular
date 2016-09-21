
angular
  .module('mainApp')
  .controller('IndexCtrl',IndexCtrl);

IndexCtrl.$inject = ['$rootScope','$scope','$window'];

function IndexCtrl($rootScope, $scope, $window) {


    //***** definir titulo principal *****
    $scope.mainTitle = null;
    $scope.setMainTitle = function(mainTitle){ $scope.mainTitle = mainTitle; };
  
  
    //***** numero entero aleatorio utilizado para evitar el almacenamiento de cache en los ng-include *****
    $scope.nocache = Math.floor((Math.random() * 100000) + 1);
  
  
    $scope.$on('$viewContentLoaded', function(event) {
      // $scope.initialize();
    });

};
