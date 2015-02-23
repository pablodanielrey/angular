
var app = angular.module('mainApp');

app.controller('EditStudentCtrl', function($scope, $timeout, Student, Session) {
  $scope.studentData = {};

  $scope.save = function() {

  }

  /**
  * Carga los datos del usuario seleccionado dentro de la sesion
  */
  $scope.loadUserData = function() {
    var s = Session.getCurrentSession();
    if (s == null) {
      return;
    }
    if (s.selectedUser == undefined || s.selectedUser == null) {
      $scope.clearUser();
    }

    var uid = s.selectedUser;

    Student.findStudentData(uid,
      function(data) {
        $scope.studentData = data.student;
      },
      function(error) {
        alert(error);
      }
    );
  }


  $timeout(function() {
    $scope.loadUserData();
  },0);

})
