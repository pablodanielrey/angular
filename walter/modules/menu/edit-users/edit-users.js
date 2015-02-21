var app = angular.module('mainApp');

app.controller('EditUsersOptionCtrl', function($scope, $rootScope) {

  $scope.visible = true;

  $scope.isVisible = function() {
    return $scope.visible;
  }

  $scope.$on('MenuOptionSelectedEvent', function(event,data) {
    $scope.visible = false;
    if (data == 'EditUsersOption') {
      $scope.visible = true;
      $rootScope.$broadcast('InitializeUserList');
    }
  });



});
