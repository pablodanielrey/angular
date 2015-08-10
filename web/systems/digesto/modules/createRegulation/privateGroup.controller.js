angular
    .module('mainApp')
    .controller('PrivateGroupCtrl',PrivateGroupCtrl)

PrivateGroupCtrl.$inject = ['$rootScope','$scope']

function PrivateGroupCtrl($rootScope,$scope) {
  $scope.initialize = initialize;

  $rootScope.$on('$viewContentLoaded', function(event) {
    $scope.initialize();
  });

  function initialize() {

  }
}
