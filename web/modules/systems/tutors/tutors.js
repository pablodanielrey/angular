
var app = angular.module('mainApp');

app.controller('TutorsCtrl', function($rootScope,$scope,$timeout,Student,Tutors,Notifications) {

  $scope.model = {
    register:{ type:'', student:{}, date:new Date() }
  };

  $scope.clearData = function() {
    $scope.model.register = { type:'', student:{}, date:new Date() };
  }

  $timeout(function() {
    $scope.clearData()
  });


  $scope.save = function() {
    Tutors.persistTutorData($scope.model.register,
      function(ok) {
        $scope.clearData();
        Notifications.message(ok);
      },
      function(error) {
        Notifications.message(error);
      }
    );
  }


});
