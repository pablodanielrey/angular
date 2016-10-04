
var app = angular.module('mainApp');

app.controller('EditStudentCtrl', ['$scope','$timeout','Student','Session','Notifications',
  function($scope, $timeout, Student, Session, Notifications) {
    $scope.student = {};

    $scope.save = function() {
      var s = Session.getCurrentSession();
      if (s == null) {
        return;
      }

      if (s.selectedUser == undefined || s.selectedUser == null) {
        return;
      }

      $scope.student.id = s.selectedUser;

      Student.persistStudent($scope.student,
  		function(student) {
  			Notifications.message("registro actualizado");
  		},
  		function(error) {
  		  Notifications.message(error);
  		}
  	);
    }


    /**
    * Carga los datos del usuario seleccionado dentro de la sesion
    */
    $scope.loadStudentData = function() {
      console.log('load data');
      var s = Session.getCurrentSession();
      if (s == null) {
        return;
      }
      if (s.selectedUser == undefined || s.selectedUser == null) {
        Notifications.message("error");
      }

      var uid = s.selectedUser;

      Student.findStudentData(uid,
        function(data) {
          $scope.student = data.student;
        },
        function(error) {
          Notifications.message(error);
        }
      );
    }

    $timeout(function() {
      $scope.loadStudentData();
    },0);
  }]
)
