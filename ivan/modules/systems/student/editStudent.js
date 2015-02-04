
var app = angular.module('mainApp');

app.controller('EditStudentCtrl', function($rootScope, $scope,Student,Session) {
  $scope.student = { number:'' };

  $scope.findStudent = function(id) {
    Student.findStudent(id,function(data) {
      $scope.student = data.student;
    },
    function(error) {
      alert(error);
    })
  }

  $scope.findCurrentStudent = function() {
    var s = Session.getCurrentSession();
    if (s == null) {
      return;
    }
    if (s.selectedUser == undefined) {
      return;
    }
    $scope.findStudent(s.selectedUser);
  }

  $rootScope.$on('UserSelectedEvent', function(e,id) {
    $scope.findStudent(id);
  });

  $scope.findCurrentStudent();

})
