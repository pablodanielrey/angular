
var app = angular.module('mainApp');

app.controller('ListGroupsCtrl',function($scope,Groups) {

  $scope.groups = [];
  $scope.selected = null;

  $scope.listGroups = function() {
    Groups.listGroups(function(gps) {
      $scope.groups = gps;
    },
    function(error) {
      alert(error);
    });
  }

  $scope.select = function(id) {
    if ($scope.isSelected(id)) {
      $scope.selected = null;
    } else {
      $scope.selected = id;
    }
  }

  $scope.isSelected = function(id) {
    return ($scope.selected == id);
  }

  setTimeout($scope.listGroups(),0);

});
