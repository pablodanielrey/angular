var app = angular.module('mainApp');

app.controller('rec', function($scope,$timeout) {

    $scope.model = {
      class:'',
      contentRecordings:false
    };


    $scope.$on('$viewRecordings', function(event) {
      $scope.model.contentRecordings = false;
    });
    // console.log('hola');
  }
);
