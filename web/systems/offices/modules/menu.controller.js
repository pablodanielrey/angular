angular
    .module('mainApp')
    .controller('MenuOfficeController',MenuOfficeController);

MenuOfficeController.$inject = ['$scope', '$timeout', '$location','Notifications'];

function MenuOfficeController($scope, $timeout, $location, Notifications) {

  var vm = this;

  vm.initialize = initialize;

  function initialize() {
    vm.selected = 'index';
  }

  $scope.$on('$viewContentLoaded', function(event) {
    vm.initialize();
  });

  $scope.$on('ItemSelected', function(event,data) {
    vm.selected = data;
  });


  // redirecciones del menu

  vm.usersOffices = usersOffices;
  vm.index = index;
  vm.rolesOffices = rolesOffices;
  vm.modifyOffice = modifyOffice;

  function usersOffices() {
    vm.selected = 'usersOffices';
    $location.path('/usersOffices');
  }

  function index() {
    vm.selected = 'index';
    $location.path('/offices');
  }

  function rolesOffices() {
    vm.selected = 'rolesOffices';
    $location.path('/rolesOffices');
  }

  function modifyOffice() {
    vm.selected = 'modifyOffice';
    $location.path('/modifyOffice');
  }

}
