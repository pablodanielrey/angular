
var app = angular.module('mainApp');


app.controller('EditGroupCtrl', function($rootScope,$scope,Groups) {

  $scope.group = null;

  $rootScope.$on('GroupSelectedEvent', function(e,id) {
    if (id == null) {
      $scope.group = null;
      return;
    }
    $scope.findGroupData(id);
  });

  $rootScope.$on('GroupUpdatedEvent', function(e,id) {
    if (($scope.group == null) || ($scope.group.id != id)) {
      return;
    }
    $scope.findGroupData(id);
  });

  $scope.update = function() {
    if ($scope.group == null) {
      return;
    }
    Groups.updateGroup($scope.group,
      function(ok) {
        // nada ya que se dispara el evento
      },
      function(err) {
        //alert(err);
      });
  }

  $scope.findGroupData = function(id) {
    Groups.findGroup(id,
      function(group) {
        $scope.group = group;
      },
      function(error) {
        //alert(error);
      }
    );
  }

});
