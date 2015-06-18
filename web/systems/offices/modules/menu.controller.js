angular
    .module('mainApp')
    .controller('MenuOfficeController',MenuOfficeController);

MenuOfficeController.$inject = ['$scope','$location','Notifications'];

function MenuOfficeController($scope, $location, Notifications) {

  var vm = this;

  vm.initialize = initialize;

  function initialize() {
  }

  $scope.$on('$viewContentLoaded', function(event) {
    vm.initialize();
  });


  // redirecciones del menu

  vm.usersOffices = usersOffices;
  vm.index = index;
  vm.rolesOffices = rolesOffices;

  function usersOffices() {
    $location.path('/usersOffices');
  }

  function index() {
    $location.path('/offices');
  }

  function rolesOffices() {
    $location.path('/rolesOffices');
  }

}
