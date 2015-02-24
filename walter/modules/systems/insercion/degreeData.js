var app = angular.module('mainApp');


app.controller('DegreeLaboralInsertionCtrl', function() {

  $scope.insertionData = {};

  $scope.$on('SaveEvent',function() {

      var saveData = { type:'degree', data:$scope.insertionData };
      $scope.emit('SaveDataEvent',saveData);

  });


});
