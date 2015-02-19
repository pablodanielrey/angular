
app.controller("AccountRequestEditCtrl", function($rootScope, $scope, Utils, Messages, Session) {

	if($rootScope.accountRequest){
		$scope.name = $rootScope.accountRequest.name;
		$scope.lastname = $rootScope.accountRequest.lastname;
		$scope.dni = $rootScope.accountRequest.dni;
		$scope.reason = $rootScope.accountRequest.reason;
		$scope.confirmed = $rootScope.accountRequest.confirmed;
		$scope.id = $rootScope.accountRequest.id;
	}
	
	$scope.$on('AccountRequestSelection', function(event,accountRequest) {
		$scope.name = accountRequest.name;
		$scope.lastname = accountRequest.lastname;
		$scope.dni = accountRequest.dni;
		$scope.reason = accountRequest.reason;
		$scope.confirmed = accountRequest.confirmed;
		$scope.id = accountRequest.id;
	});

	$scope.clearForm = function(){
		$scope.name = "";
		$scope.lastname = "";
		$scope.dni = "";
		$scope.reason = "";
		$scope.confirmed = false;
		$scope.id = "";
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
			"description" : $scope.description,
			"action" : "rejectAccountRequest",
		};

		Messages.send(msg,function(response) {
			$rootScope.$broadcast('AccountRequestUpdated');
		});

		$scope.clearForm();
	}

});
