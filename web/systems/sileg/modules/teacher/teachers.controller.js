angular
  .module('mainApp')
  .controller('TeachersCtrl', TeachersCtrl);

TeachersCtrl.inject = []

function TeachersCtrl($rootScope, $scope, $timeout, $wamp, Sileg, UserFormat) {

    $scope.user = null;
    $scope.cathedra = null;

 
}
