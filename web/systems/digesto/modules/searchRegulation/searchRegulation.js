angular
    .module('mainApp')
    .controller('SearchRegulationCtrl',SearchRegulationCtrl)

SearchRegulationCtrl.$inject = ['$rootScope','$scope']

function SearchRegulationCtrl($rootScope,$scope) {

  $scope.initialize = initialize;

  $rootScope.$on('$viewContentLoaded', function(event) {
    $scope.initialize();
  });

  function initialize() {

  }
}
