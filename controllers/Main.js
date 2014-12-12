
app.controller("MainController", ["$scope", function($scope) {
	$scope.showMessage = false;
	
	$scope.$on('showMessage', function(event, msg) { 
		$scope.message = msg;
		$scope.showMessage = true;
	});
	
	$scope.$on('dontShowMessage', function(event, msg) { 
		$scope.message = "";
		$scope.showMessage = false;
	});
}]); 
