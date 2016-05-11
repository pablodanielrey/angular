
angular
  .module('mainApp')
  .controller('IndexCtrl',IndexCtrl);

IndexCtrl.$inject = ['$rootScope','$scope','$window'];

function IndexCtrl($rootScope, $scope, $window) {

    $scope.$on('$viewContentLoaded', function(event) {
      // $scope.initialize();
    });

};
