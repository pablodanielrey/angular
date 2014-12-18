
app.factory('Session', ["$rootScope", "$cookies", "$location", function($rootScope, $cookies, $location){
		
	var factory = {};
	
	/**
	 * Ir a la pagina de inicio que variara en funcion de si existe sesion o no
	 */
	factory.goHome = function(){
		if(($cookies.fceSession != undefined) 
		&& ($cookies.fceSession != "") 
		&& ($cookies.fceSession != null)
		&& ($cookies.fceSession != false)){
			$location.path("/home");				
		} else {
			$location.path("/login");	
		}
	};
	
	factory.create = function(session){
		$cookies.fceSession = session;
		this.goHome();
	}
	
	/**
	 * Destruir session
	 */
	factory.destroy = function(){
		$cookies.fceSession = "";
		this.goHome();
	};
	
	
	return factory;
}]);
