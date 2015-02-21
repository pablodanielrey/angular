
app.controller("AccountRequestsListCtrl", function($rootScope, $scope, Utils, Session, Messages) {

	//inicializar filtro
	$scope.filterconfirmed = [];
	$scope.filterconfirmed.confirmed = true;
	$scope.filterconfirmed.unconfirmed = true;


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
	$scope.selectAccountRequest = function(accountRequest){
		var s = Session.getCurrentSession();
		s.accountRequestSelected = accountRequest;
		Session.saveSession(s);

		$scope.accountRequestSelected = accountRequest;

		$rootScope.$broadcast('AccountRequestSelection',accountRequest);
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

	$scope.$on('InitializeAccountRequestList', function() {
		//llamar a la lista de AccountRequests
		$scope.listAccountRequests();
	});

});
