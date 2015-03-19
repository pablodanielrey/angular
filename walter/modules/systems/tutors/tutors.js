
var app = angular.module('mainApp');

app.controller('TutorsCtrl', function($rootScope,$scope,$timeout,Student,Tutors,Notifications) {

  $scope.model = {
    register:{ type:'', studentNumber:'', date:new Date() },
    students:[]
  };

  $timeout(function() {
    $scope.findStudents();
  });

  $scope.findStudents = function() {
    Student.findAllStudentsData(
      function(response) {
        $scope.model.students = response.students;
        $scope.model.students.sort();
        if ($scope.model.students.length > 0) {
          $scope.model.register.studentNumber = $scope.model.students[0].studentNumber;
        }
      },
      function(error) {
        alert(error);
      }
    );
  }

  $scope.save = function() {
    Tutors.persistTutorData($scope.model.register,
      function(ok) {
        Notifications.message(ok);
      },
      function(error) {
        Notifications.message(error);
      }
    );
  }


});
