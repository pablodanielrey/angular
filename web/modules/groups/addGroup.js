
var app = angular.module('mainApp');


app.controller('AddGroupCtrl', function($scope, Groups, Systems) {

  $scope.group = { systemId: '', name: '' };
  $scope.systems = [];

  $scope.clear = function() {
    $scope.group = { systemId: '', name: '' };
  }

  $scope.add = function() {
    if ($scope.group.name == '') {
      return;
    }

    Groups.createGroup($scope.group,
      function(ok) {
        $scope.clear();
      },
      function(error) {
        alert(error);
      });
  }


  $scope.findSystems = function() {
    Systems.listSystems(
      function(systems) {
        $scope.systems = systems;
      },
      function(err) {
        alert(err);
      });
  }

  setTimeout(function() { $scope.findSystems(); },0);

});
