
app.controller("AccountRequestsListCtrl", function($rootScope, $scope, Utils, Session, Messages) {

	//inicializar filtro
	$scope.filterconfirmed = [];
	$scope.filterconfirmed.confirmed = true;
	$scope.filterconfirmed.unconfirmed = false;
	$scope.filterconfirmed.rejected = false;

	/**
	 * Manejo del evento AccountRequestApproved: Cuando se aprueba una cuenta se debe actualizar la lista de requerimientos
	 */
	$scope.$on('AccountRequestUpdated', function(event,data) {
		$scope.listAccountRequests();
	});

	/**
	 * Seleccionar un requerimiento de cuenta para su edicion, denegacion o aprobacion
	 * @param accountRequestId
	 * 
	 */
	$scope.selectAccountRequest = function(accountRequestId){
		$rootScope.$broadcast('AccountRequestSelection',accountRequestId);
	};
	
	/**
	 * Definir lista de requerimientos de cuenta
	 * 
	 */
	$scope.listAccountRequests = function(){

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
