
var app = angular.module('mainApp');

app.controller('TutorsCtrl', function($scope) {

  $scope.model = {
    register:{ type:'', student:'', date:new Date() },
    students:[]
  };


});
