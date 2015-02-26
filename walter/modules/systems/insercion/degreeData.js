var app = angular.module('mainApp');


app.controller('DegreeLaboralInsertionCtrl', function($scope, $timeout, LaboralInsertion) {

  $scope.$on('UpdateUserDataEvent',function(event,data) {
    $scope.loadData();
  });


  $scope.loadData = function() {

    LaboralInsertion.findDegreeData($scope.selectedUser,
      function(data) {
        $scope.degrees = data;
      },
      function(err) {
        alert(err);
      });

  }

  $timeout(function() {
    $scope.loadData();
  });


});
