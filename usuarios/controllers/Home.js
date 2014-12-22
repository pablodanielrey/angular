
app.controller("HomeController", ["Session", "$location", function(Session, $location){

	if((Session.getSessionId() != undefined) 
	&& (Session.getSessionId() != "")){
		$location.path("/home");				
	} else {
		$location.path("/login");	
	}
}]); 
