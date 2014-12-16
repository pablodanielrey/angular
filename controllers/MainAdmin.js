
app.controller("MainAdminController", ["$rootScope", "$scope", function($rootScope, $scope) {
	$scope.showMessage = false;
	$rootScope.socketOpen = false;
	$rootScope.session = null;
	$rootScope.target = "listCreateAccount"
		
	$scope.$on('socketOnOpen', function(event, msg) {
		$rootScope.socketOpen = true;
	});
	
	$scope.$on('showMessage', function(event, msg) { 
		$scope.message = msg;
		$scope.showMessage = true;
	});
	
	$scope.$on('dontShowMessage', function(event, msg) { 
		$scope.message = "";
		$scope.showMessage = false;
	});
}]); 
