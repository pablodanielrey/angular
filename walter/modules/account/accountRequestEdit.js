
app.controller("AccountRequestEditCtrl", function($rootScope, $scope, Utils, Messages, Session) {

	$scope.showAccountRequestEdit = false;
	
	$scope.container = {
	    'display':'none'
	};
	
	$scope.$on('AccountRequestSelection', function(event,accountRequest) {
		$scope.name = accountRequest.name;
		$scope.lastname = accountRequest.lastname;
		$scope.dni = accountRequest.dni;
		$scope.reason = accountRequest.reason;
		$scope.confirmed = accountRequest.confirmed;
		$scope.id = accountRequest.id;
		$scope.showAccountRequestEdit = true;
	});
	
	$scope.clearForm = function(){
		$scope.name = "";
		$scope.lastname = "";
		$scope.dni = "";
		$scope.reason = "";
		$scope.confirmed = false;
		$scope.id = "";
		$scope.showAccountRequestEdit = false;
	}

	$scope.approveAccountRequest = function(){
		var msg = {
			"id" : Utils.getId(),
			"reqId" : $scope.id,
			"session" : Session.getSessionId(),
			"action" : "approveAccountRequest",
		};

		Messages.send(msg,function(response) {
			$rootScope.$broadcast('AccountRequestUpdated');
		});
		
		$scope.clearForm();
	};

	$scope.removeAccountRequest = function() {	
		var msg = {
			"id" : Utils.getId(),
			"reqId" : $scope.id,
			"session" : Session.getSessionId(),
			"action" : "removeAccountRequest",
		};
		
		
		Messages.send(msg,function(response) {
			$rootScope.$broadcast('AccountRequestUpdated');
		});
		
		$scope.clearForm();
	};
	
	$scope.rejectAccountRequest = function(){
		var msg = {
			"id" : Utils.getId(),
			"reqId" : $scope.id,
			"session" : Session.getSessionId(),
			"action" : "rejectAccountRequest",
		};
		
		Messages.send(msg,function(response) {
			$rootScope.$broadcast('AccountRequestUpdated');
		});
		
		$scope.clearForm();
	}
	
});
