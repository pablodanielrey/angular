
app.controller("AccountRequestsListCtrl", function($rootScope, $scope, Utils, Session, Messages) {

	//inicializar filtro
	$scope.filterconfirmed = [];
	$scope.filterconfirmed.confirmed = true;
	$scope.filterconfirmed.unconfirmed = false;

	/**
	 * Manejo del evento AccountRequestApproved: Cuando se aprueba una cuenta se debe actualizar la lista de requerimientos
	 */
	$scope.$on('AccountRequestUpdated', function(event,data) {
		$scope.requests = [];
		$scope.listAccountRequests();
	});

	/**
	 * Seleccionar un requerimiento de cuenta para su edicion, denegacion o aprobacion
	 * @param accountRequestId
	 * 
	 */
	$scope.selectAccountRequest = function(requestId){
		var requestAccount = Utils.filter(function(e) {
			return e.id == requestId;
		}, $scope.requests)[0];
		
		$scope.accountRequestSelected = requestAccount.id;
		$rootScope.$broadcast('AccountRequestSelection',requestAccount);
	};
	
	
	$scope.isSelected = function(id) {
		return $scope.accountRequestSelected == id;
	}
	
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
