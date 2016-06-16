
var app = angular.module('mainApp');

app.controller('ListGroupsCtrl',function($rootScope,$scope,Groups) {

  $scope.groups = [];
  $scope.selected = null;

  $rootScope.$on('GroupCreatedEvent', function(e,id) {
    $scope.listGroups();
  });

  $rootScope.$on('GroupUpdatedEvent', function(e,id) {
    $scope.listGroups();
  });


  $scope.listGroups = function() {
    Groups.listGroups(function(gps) {
      $scope.groups = gps;
    },
    function(error) {
      //alert(error);
    });
  }

  $scope.select = function(id) {
    if ($scope.isSelected(id)) {
      $scope.selected = null;
      $rootScope.$broadcast('GroupSelectedEvent',null);
    } else {
      $scope.selected = id;
      $rootScope.$broadcast('GroupSelectedEvent',$scope.selected);
    }
  }

  $scope.isSelected = function(id) {
    return ($scope.selected == id);
  }

  setTimeout($scope.listGroups(),0);

});
