

/*
	Lista de los pedidos de creación de cuentas de la facultad.

	eventos escuchados :

		NewAccountRequestEvent
		AccountRequestApprovedEvent
		AccountRequestRemovedEvent


*/


app.controller("ListAccountRequestsCtrl", function($rootScope, $scope, Messages, Session, Utils) {

	$scope.requests = [];

	$scope.$on('NewAccountRequestEvent', function(event,data) {
		$scope.listAccountRequests();
	});

	$scope.$on('AccountRequestConfirmedEvent', function(event,data) {
		$scope.listAccountRequests();
	});

	$scope.$on('AccountRequestApprovedEvent', function(event,data) {
		$scope.listAccountRequests();
	});

	$scope.$on('AccountRequestRemovedEvent', function(event,data) {
		$scope.listAccountRequests();
	});

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
			"action" : "approveAccountRequest",
		};
		Messages.send(msg,function(response) {
				$scope.listAccountRequests();
		});
	};

	$scope.removeRequest = function(id) {
		var msg = {
			"id" : Utils.getId(),
			"reqId" : id,
			"session" : Session.getSessionId(),
			"action" : "removeAccountRequest",
		};
		Messages.send(msg,function(response) {
			$scope.listAccountRequests();
		});
	}



	$scope.listAccountRequests();

});
