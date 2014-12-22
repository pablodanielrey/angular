
app.controller("HomeController", ["Session", "$location", function(Session, $location){

	Session.goHome();
	
	if((Session.getSessionId() != undefined) 
	&& (Session.getSessionId() != "")){
		$location.path("/home");				
	} else {
		$location.path("/login");	
	}
}]); 
