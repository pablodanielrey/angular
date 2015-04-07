var app = angular.module('mainApp');

app.controller('AssistanceFailsCtrl', function($scope, $timeout, Notifications, Assistance) {

  $scope.model = {
    begin: new Date(),
    end: new Date(),
    assistanceFails:[{}]
  }

  $scope.initialize = function() {
    $scope.model.begin = new Date();
    $scope.model.end = new Date();
    $scope.model.assistanceFails = [{}]
  }

  $scope.search = function() {
    $scope.model.assistanceFails = [{}];
    $scope.model.end.setHours(23);
    $scope.model.end.setMinutes(59);
    $scope.model.begin.setHours(0);
    $scope.model.begin.setMinutes(0);
    console.log($scope.model.begin);
    console.log($scope.model.end);
    Assistance.getFailsByDate($scope.model.begin, $scope.model.end,
      function(response) {
        for (var i = 0; i < response.length; i++) {
          var r = response[i];
          r.fail.dateFormat = new Date(r.fail.date).toLocaleDateString();
          $scope.model.assistanceFails.push(r);
        }
      }, function(error) {
        Notification.message(error);
      }

    );
  }

  $timeout(function() {
    $scope.initialize();
  }, 0);

});
