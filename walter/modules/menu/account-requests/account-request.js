var app = angular.module('mainApp');

app.controller('AccountRequestOptionCtrl', function($rootScope, $scope, $location) {

  $scope.visible = false;

  $scope.isVisible = function() {
    return $scope.visible;
  }

  $scope.$on('MenuOptionSelectedEvent', function(event,data) {
    $scope.visible = false;
    if (data == 'AccountRequestsOption') {
      $scope.visible = true;
      $rootScope.$broadcast('InitializeAccountRequestList');
    }
  });

  $scope.$on('AccountRequestSelection',function(event,data) {
    $location.path('/editAccountRequest');
  });

})
