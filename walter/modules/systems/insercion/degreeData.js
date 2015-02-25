var app = angular.module('mainApp');


app.controller('DegreeLaboralInsertionCtrl', function($scope) {

  $scope.$on('SaveEvent',function() {

      var saveData = { type:'degree', data:$scope.insertionData };
      $scope.$emit('SaveDataEvent',saveData);

  });


});
