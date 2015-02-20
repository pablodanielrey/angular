
app.controller("AccountRequestEditCtrl", function($rootScope ,$scope, Utils, Messages, Session) {
	
	$scope.session = Session.getCurrentSession();

/*
	if (($scope.session != null) && ($scope.session.accountRequest != null) && ($scope.session.accountRequest != undefined)) {
		$scope.name = $scope.session.accountRequest.accountRequest.name;
		$scope.lastname = $scope.session.accountRequest.accountRequest.lastname;
		$scope.dni = $scope.session.accountRequest.accountRequest.dni;
		$scope.reason = $scope.session.accountRequest.accountRequest.reason;
		$scope.confirmed = $scope.session.accountRequest.accountRequest.confirmed;
		$scope.id = $scope.session.accountRequest.accountRequest.id;
    }
*/
	
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
