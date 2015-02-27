var app = angular.module('mainApp');


app.controller('DegreeLaboralInsertionCtrl', function($scope, $timeout, LaboralInsertion) {

  $scope.$on('UpdateUserDataEvent',function(event,data) {
    $scope.loadData();
  });


  $scope.loadData = function() {

    LaboralInsertion.findDegreeData($scope.model.selectedUser,
      function(data) {
        if ((data != undefined) && (data != null) && (data.length > 0)) {
          $scope.model.degrees = data;
        }
      },
      function(err) {
        alert(err);
      });

  }

  $timeout(function() {
    $scope.loadData();
  });


});
