
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



	$scope.approveAccount = function(accountId){
		var id = uuid4.generate();
		ids[id] = "aprobeCreateRequest";

		var data = {
			"id" : id,
			"reqId" : accountId,
			"session" : Session.getSessionId(),
			"action" : "aprobeCreateRequest",
		};

	};

	$scope.approveSelectedAccounts = function(){
		alert("en construccion");
	};

	$scope.selectAccount = function(accountId){
		var idRow = document.getElementById("account"+accountId);

		if(accountsSelected[accountId] == undefined){
			accountsSelected[accountId] = true;
			idRow.className = "selected";
		} else {
			delete accountsSelected[accountId];
			idRow.className = "";
		}
	};



	$scope.listAccountRequests();

});
