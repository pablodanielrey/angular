
var app = angular.module('mainApp');


app.controller('EditGroupCtrl', function($rootScope,$scope,Groups) {

  $scope.group = null;

  $rootScope.$on('GroupSelectedEvent', function(e,id) {
    if (id == null) {
      $scope.group = null;
      return;
    }
    Groups.findGroup(id,
      function(group) {
        $scope.group = group;
      },
      function(error) {
        alert(error);
      })
    });


});
