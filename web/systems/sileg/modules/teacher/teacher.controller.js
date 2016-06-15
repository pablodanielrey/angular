angular
  .module('mainApp')
  .controller('TeacherCtrl', TeacherCtrl);

TeacherCtrl.inject = ['$rootScope', '$scope', '$timeout', '$wamp', 'Sileg']

function TeacherCtrl($rootScope, $scope, $timeout, $wamp, Sileg) {

  console.log("test");
}
