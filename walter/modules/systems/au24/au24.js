var app = angular.module('mainApp');

app.controller("Au24Ctrl", ["$scope", "$rootScope", "$timeout", "Au24", "Session", function($scope, $rootScope, $timeout, Au24, Session) {


/**
 * Cargar datos de au24 en funcion del usuario seleccionado
 * @session selectedUser Se utiliza la variable de session con el usuario seleccionado para buscar los datos asociados de au 24
 */	
$scope.loadAu24Data = function() {
	var session = Session.getCurrentSession();
    
    if (session == null) {
      return;
    }
    
    if (session.selectedUser == undefined || session.selectedUser == null) {
      return;
	}
    
    
	Au24.findAu24ByUserId(session.selectedUser,
	
		/**
		 * callback ok
		 * @param au24 Datos de au24 correspondientes al usuario
		 */
		function(au24) {


		},
		
		/**
		 * callback error
		 * @param error String con la descripcion del error
		 */
		function(error) {
			alert(error);
		}
    );
    
}

	
$timeout(function() { 
	$scope.loadAu24Data(); 
},0);


	
}]);
