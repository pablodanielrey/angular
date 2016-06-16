angular
    .module('mainApp')
    .controller('LogController',LogController);

LogController.$inject = ["$rootScope","$scope","$timeout", "$location"];

function LogController($rootScope, $scope, $timeout, $location) {

  var vm = this;

  vm.model = {
    user: {},
    date: new Date(),
    hours: ''
  }

  vm.setDate = setDate;
  vm.initialize = initialize;


  // ////////////////////////////////////////////////////////////////
  // ////////////////////// EVENTS //////////////////////////////////
  // ////////////////////////////////////////////////////////////////

  $scope.$on('$viewContentLoaded', function(event) {
    vm.initialize();
  });


  // ////////////////////////////////////////////////////////////////
  // ////////////////////// FUNCTIONS ///////////////////////////////
  // ////////////////////////////////////////////////////////////////

  function initialize() {
      vm.model.date = ($scope.$parent.logData && $scope.$parent.logData.date) ? $scope.$parent.logData.date : new Date();
      vm.model.user = ($scope.$parent.logData && $scope.$parent.logData.user) ? $scope.$parent.logData.user : {};

      vm.setDate();

      $timeout(function() {
        $location.path('/firmware');
      }, 5000);
  }

  function setDate() {
    var hs = ('0' + vm.model.date.getHours()).slice(-2);
    var min = ('0' + vm.model.date.getMinutes()).slice(-2);
    vm.model.hours = hs + ":" + min;
  }




}
