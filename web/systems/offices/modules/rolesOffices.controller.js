angular
    .module('mainApp')
    .controller('RolesOfficesController',RolesOfficesController);

RolesOfficesController.$inject = ['$scope','$location','Notifications'];

function RolesOfficesController($scope, $lcoation, Notifcations) {

  var vm = this;

  vm.initialize = initialize;

  function initialize() {

  }

  $scope.$on('$viewContentLoaded', function(event) {
    $scope.$parent.itemSelected('rolesOffices');
    vm.initialize();
  });

}
