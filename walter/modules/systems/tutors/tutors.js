
var app = angular.module('mainApp');

app.controller('TutorsCtrl', function($rootScope,$scope,$timeout,Student,Tutors) {

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
        response.students.sort();
        $scope.model.students = response.students;
        if (response.students.length > 0) {
          $scope.model.register.studentNumber = response.students[0].studentNumber;
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
        $rootScope.$broadcast('ShowMessageEvent',ok);
      },
      function(error) {
        $rootScope.$broadcast('ShowMessageEvent',error);
      }
    );
  }


});
