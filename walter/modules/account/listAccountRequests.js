
app.controller("ListAccountRequestsCtrl", function($rootScope, $scope, Messages, Session, Utils) {

	$scope.requests = [];

	$scope.listAccountRequests = function() {

		var msg = {
			id: Utils.getId(),
			session : Session.getSessionId(),
			action : "listAccountRequests",
		}

		Messages.send(msg, function(response) {

			if (response.requests == undefined) {
				$scope.requests = [];
				return;
			}

			$scope.requests = response.requests;
		});

	}

	$scope.approveRequest = function(accountId){

		var msg = {
			"id" : Utils.getId(),
			"reqId" : accountId,
			"session" : Session.getSessionId(),
			"action" : "aprobeRequest",
		};

		Messages.send(msg,function(response) {
				$scope.listAccountRequests();
		});

	};

	$scope.listAccountRequests();

});
