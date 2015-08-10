angular
    .module('mainApp')
    .controller('RelatedsCtrl',RelatedsCtrl)

    RelatedsCtrl.$inject = ['$rootScope','$scope']

function RelatedsCtrl($rootScope,$scope) {
  $scope.initialize = initialize;

  $rootScope.$on('$viewContentLoaded', function(event) {
    $scope.initialize();
  });

  function initialize() {

  }
}
