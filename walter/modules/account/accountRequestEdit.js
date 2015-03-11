
app.controller("AccountRequestEditCtrl", function($rootScope, $scope, $timeout, Utils, Messages, Session) {

	$scope.initialize = function() {
		$scope.clearForm();
		var s = Session.getCurrentSession();
		if (s.accountRequestSelected == null) {
			return;
		}
		$scope.accountRequest = s.accountRequestSelected;
	}

	$scope.clearForm = function(){
		$scope.accountRequest = {};
	}

	$scope.approveAccountRequest = function(){
		var msg = {
			"id" : Utils.getId(),
			"reqId" : $scope.accountRequest.id,
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
			"reqId" : $scope.accountRequest.id,
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
			"reqId" : $scope.accountRequest.id,
			"session" : Session.getSessionId(),
			"description" : $scope.description,
			"action" : "rejectAccountRequest",
		};

		Messages.send(msg,function(response) {
			$rootScope.$broadcast('AccountRequestUpdated');
		});

		$scope.clearForm();
	}


	$scope.$on('AccountRequestSelection', function(event,data) {
		$scope.initialize();
	});

	$timeout(function() {
		console.log('timeout');
		$scope.initialize();
	},0);

});
