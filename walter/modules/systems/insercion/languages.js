var app = angular.module('mainApp');


app.controller('LanguageLaboralInsertionCtrl', function() {

  $scope.insertionData = {};


  $scope.$on('SaveEvent',function() {

    var saveData = { type:'language', data:$scope.insertionData };
    $scope.emit('SaveDataEvent',saveData);

  });


});
