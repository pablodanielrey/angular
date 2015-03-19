
var app = angular.module('mainApp');

app.controller('TutorsCtrl', function($scope,$timeout,Student,Tutors) {

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


  $scope.save = function() {
    Tutors.persistTutorData($scope.model.register,
      function(ok) {

      },
      function(error) {

      }
    );
  }


});
