
/**
 * Controlador para realizar login
 * @param $scope Scope
 * Supone la existencia de un elemento padre que maneja los eventos dontShowMessage y showMessage para administrar mensajes
 */
app.controller("HomeController", ["$scope",  function($scope){

	var data = {
		"action" : "goHome",
	}
		
	$scope.$emit("onEvent", JSON.stringify(data));
	
}]); 
