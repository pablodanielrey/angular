var app = angular.module('mainApp');

app.controller('MessagesCtrl',function($scope,$timeout) {

  $scope.visible = false;
  $scope.messages = [];

  $scope.$on('ShowMessageEvent',function(event,data) {

    if (typeof data === 'string') {
      $scope.messages = [];
      $scope.messages.push(data);
    } else {
      $scope.messages = data;
    }

    $scope.visible = true;
    $timeout(function() {
      $scope.visible = false;
    }, 5000);
  });


  $scope.isVisible = function() {
    return $scope.visible;
  }


  $scope.accept = function() {
    $scope.visible = false;
  }

});
