angular
    .module('mainApp')
    .controller('UsersOfficesController',UsersOfficesController);

UsersOfficesController.$inject = ['$scope','$location','Notifications'];

function UsersOfficesController($scope, $location, Notifications) {

  var vm = this;

  vm.initialize = initialize;

  function initialize() {

  }

  $scope.$on('$viewContentLoaded', function(event) {
    vm.initialize();
  });
    
}
