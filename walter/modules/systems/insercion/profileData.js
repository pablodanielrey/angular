var app = angular.module('mainApp');


app.controller('ProfileLaboralInsertionCtrl', function() {

  $scope.insertionData = {};
  $scope.user = {};

  $scope.$on('SaveEvent',function() {

    var saveData = { type:'profile', data:$scope.user };
    $scope.emit('SaveDataEvent',saveData);

  });


});
