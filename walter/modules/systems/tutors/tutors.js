
var app = angular.module('mainApp');

app.controller('TutorsCtrl', function($scope,$timeout,Student) {

  $scope.model = {
    register:{ type:'', student:'', date:new Date() },
    students:[]
  };


  $timeout(function() {
    Student.findAllStudentsData(
      function(response) {
        $scope.model.students = response.students;
      },
      function(error) {
        alert(error);
      }
    );
  });

});
