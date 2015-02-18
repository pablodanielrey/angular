var app = angular.module('mainApp');


/**
 * Controlador para la edicion del estudiante
 * 
 * @service $scope
 * @service Session
 */
app.controller("StudentFormCtrl", ["$scope", "Session", function($scope, Session) { 
	
	var session = Session.getCurrentSession();
	
		
	/**
	 * Obtener datos de estudiante
	 *
	 */
	var getStudentData = function(){
		//TODO buscar datos de alumno en base al id de usuario
		
	};
	
	/**
	 * Codigo de ejecucion principal
	 */
	if((session.selectedUser == null) || (session.selectedUser == undefined)){
		session.selectedUser = session.user_id;
		Session.saveSession(session);
	};
	
	getStudentData();
	
}]); 
