angular
  .module('mainApp')
  .controller('IndexLoginCtrl',IndexLoginCtrl);

IndexLoginCtrl.$inject = ['$rootScope','$scope','$location','Notifications'];

function IndexLoginCtrl($rootScope, $scope, $location, Notifications) {

    var vm = this;

    $scope.model = {
    }

    $scope.initialize = function() {
    }

    $scope.$on('$viewContentLoaded', function(event) {
      $scope.initialize();
    });
};
