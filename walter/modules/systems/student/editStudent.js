
var app = angular.module('mainApp');

app.controller('EditStudentCtrl', function($scope, $timeout, Student, Session) {
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
			alert("registro actualizado");
		},
		function(error) {
			alert(error);
		}
	);
  }
 

  /**
  * Carga los datos del usuario seleccionado dentro de la sesion
  */
  $scope.loadStudentData = function() {
    var s = Session.getCurrentSession();
    if (s == null) {
      return;
    }
    if (s.selectedUser == undefined || s.selectedUser == null) {
      alert("error");
    }

    var uid = s.selectedUser;

    Student.findStudentData(uid,
      function(data) {
        $scope.student = data.student;
      },
      function(error) {
        alert(error);
      }
    );
  }


  $timeout(function() {
    $scope.loadStudentData();
  },0);
  
  

})
