angular
    .module('mainApp')
    .controller('MainOfficeController',MainOfficeController);

MainOfficeController.$inject = ['$scope','$location','Notifications'];

function MainOfficeController($scope, $location, Notifications) {

  var vm = this;

  vm.initialize = initialize;

  function initialize() {
    vm.elem = 'Emanuel';
  }

  $scope.$on('$viewContentLoaded', function(event) {
    vm.initialize();
  });


  // redirecciones del menu

  vm.usersOffices = usersOffices;

  function usersOffices() {
    $location.path('/usersOffices');
  }

}
