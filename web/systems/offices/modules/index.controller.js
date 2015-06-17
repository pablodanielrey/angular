angular
    .module('mainApp')
    .controller('MainOfficeController',MainOfficeController);

MainOfficeController.$inject = ['$scope','$location','Notifications'];

function MainOfficeController($scope, $location, Notifications) {

  var vm = this;

  vm.initialize = initialize;

  console.log('controller');

  function initialize() {
    console.log('initialize');
    vm.elem = 'Emanuel';
  }

  $scope.$on('$viewContentLoaded', function(event) {
    vm.initialize();
  });

}
