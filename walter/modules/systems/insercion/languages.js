var app = angular.module('mainApp');


app.controller('LanguagesLaboralInsertionCtrl', function($scope) {

  $scope.insertionData = {};

  $scope.$on('SaveEvent',function() {

    var saveData = { type:'language', data:$scope.insertionData };
    $scope.$emit('SaveDataEvent',saveData);

  });


});
