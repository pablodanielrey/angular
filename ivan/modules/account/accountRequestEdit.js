
app.controller("AccountRequestEditCtrl", function($rootScope, $scope, Utils, Messages, Session) {

	$scope.container = {
	    'display':'none'
	};
		
	$scope.$on('AccountRequestSelection', function(event,data) {
		$scope.id = data;

		$scope.container = {
		    'display':'block'
		};
	});

	$scope.approveAccountRequest = function(){

		var msg = {
			"id" : Utils.getId(),
			"reqId" : $scope.id,
			"session" : Session.getSessionId(),
			"action" : "approveAccountRequest",
		};

		Messages.send(msg,function(response) {
			$scope.container = {
				'display':'none'
			};
			$rootScope.$broadcast('AccountRequestUpdated');
		});
	};

	$scope.removeAccountRequest = function() {
		var msg = {
			"id" : Utils.getId(),
			"reqId" : $scope.id,
			"session" : Session.getSessionId(),
			"action" : "removeAccountRequest",
		};
		Messages.send(msg,function(response) {
			$scope.container = {
				'display':'none'
			};
			$scope.listAccountRequests('AccountRequestUpdated');
		});
	};
	
	$scope.rejectAccountRequest = function(){
		var msg = {
			"id" : Utils.getId(),
			"reqId" : $scope.id,
			"session" : Session.getSessionId(),
			"action" : "rejectAccountRequest",
		};
		Messages.send(msg,function(response) {
			$scope.listAccountRequests('AccountRequestUpdated');
		});
	}
	
});
