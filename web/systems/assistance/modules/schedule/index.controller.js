angular
  .module('mainApp')
  .controller('ScheduleCtrl', ScheduleCtrl);

ScheduleCtrl.inject = ['$scope', 'Login', 'Assistance', 'Users', 'Office', '$location', '$timeout']

function ScheduleCtrl($scope, Login, Assistance, Users, Office, $location, $timeout) {
}
