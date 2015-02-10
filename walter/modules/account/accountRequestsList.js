
app.controller("AccountRequestsListCtrl", function($scope, Utils, Session, Messages) {

	//inicializar filtro
	$scope.filterconfirmed = [];
	$scope.filterconfirmed.confirmed = true;
	$scope.filterconfirmed.unconfirmed = false;

	/**
	 * Definir lista de requerimientos de cuenta
	 * 
	 */
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
	};
	
	//llamar a la lista de AccountRequests
	$scope.listAccountRequests();

});
