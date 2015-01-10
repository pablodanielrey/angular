
var app = angular.module('mainApp');

app.controller('ListGroupsCtrl',function($scope,Groups) {

  $scope.groups = [];

  $scope.listGroups = function() {
    Groups.listGroups(function(gps) {
      $scope.groups = gps;
    },
    function(error) {
      alert(error);
    });
  }

  $scope.listGroups();

});
