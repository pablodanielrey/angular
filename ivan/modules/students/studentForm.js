var app = angular.module('mainApp');


/**
 * Controlador para la edicion del estudiante
 * 
 * @service $scope
 * @service Session
 */
app.controller("StudentFormCtrl", ["$scope", "Session", function($scope, Session) { 
	
	/**
	 * Obtener datos de estudiante
	 *
	 */
	var getStudentData = function(){
		alert("Datos de prueba");
		$scope.student = new Array();
		$scope.student.studentNumber = "11111/2";
		$scope.student.degrees = new Array();
		$scope.student.degrees[0] = Array();
		$scope.student.degrees[0]["name"] = "Test";
		
	};

	var session = Session.getCurrentSession();

	if((session.selectedUser == null) || (session.selectedUser == undefined)){
		session.selectedUser = session.user_id;
		Session.saveSession(session);
	};

	getStudentData();
	
}]); 
