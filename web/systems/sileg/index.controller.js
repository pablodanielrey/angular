
angular
  .module('mainApp')
  .controller('IndexCtrl',IndexCtrl);

IndexCtrl.$inject = ['$rootScope','$scope','$window'];

function IndexCtrl($rootScope, $scope, $window) {


    //***** numero entero aleatorio utilizado para evitar el almacenamiento de cache en los ng-include *****
    $scope.nocache = Math.floor((Math.random() * 100000) + 1);
  
  
    $scope.$on('$viewContentLoaded', function(event) {
      // $scope.initialize();
    });

};
