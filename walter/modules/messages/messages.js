var app = angular.module('mainApp');

app.controller('MessagesCtrl',function($scope,$timeout) {

  $scope.visible = false;
  $scope.messages = [];
  $scope.callback = null;

  $scope.$on('ShowMessageEvent',function(event,msgs) {

    $scope.messages = msgs.messages;

    $scope.visible = true;
    $timeout(function() {
      $scope.visible = false;
      $scope.callCallback();
    }, 5000);
  });


  $scope.callCallback = function() {
    if ($scope.callback != null) {
      var c = callback;
      $scope.callback = null;
      c();
    }
  }

  $scope.isVisible = function() {
    return $scope.visible;
  }

  $scope.accept = function() {
    $scope.visible = false;
    $scope.callCallback();
  }

});
