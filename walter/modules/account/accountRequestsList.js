
app.controller("AccountRequestsListCtrl", function($rootScope, $scope, Utils, Account, Session) {

	//inicializar filtro
	$scope.filterconfirmed = [];
	$scope.filterconfirmed.confirmed = true;
	$scope.filterconfirmed.unconfirmed = true;
	$scope.filterDescription = [];
	$scope.filterDescriptionSelected = null;


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
	$scope.selectAccountRequest = function(accountRequest) {
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
	$scope.listAccountRequests = function() {

		Account.listAccounts(
			function(response) {
				if (response == undefined) {
					$scope.requests = [];
					return;
				}
				$scope.requests = response;
				$scope.loadFilterDescription();
			},
			function(error) {
				alert(error);
			});
	};


	$scope.loadFilterDescription = function() {
		$scope.filterDescription = [];
		$scope.addFilterDescription(null);
		for (var i = 0; i < $scope.requests.length; i++) {
			var r = $scope.requests[i];
			$scope.addFilterDescription(r);
		}
		$scope.filterDescriptionSelected = $scope.filterDescription[0];
	};

	$scope.addFilterDescription = function(r) {
		if (r == null) {
			$scope.filterDescription.push({label:'Todos',value:'all',items:$scope.requests});
			return;
		}
		for (var i=0; i<$scope.filterDescription.length; i++) {
			var d = $scope.filterDescription[i];
			if (d.label == r.reason) {
				d.items.push(r);
				return;
			}
		}
		var desciption = {label:r.reason,items:[r],value:r.reason};
		$scope.filterDescription.push(desciption);
	}

	$scope.onChangeFilterDescription = function(selected) {
		$scope.requests = selected.items;
		if ($scope.accountRequestSelected != null) {
			$scope.selectAccountRequest(null);
		}
	}

	$scope.$on('InitializeAccountRequestList', function() {
		//llamar a la lista de AccountRequests
		$scope.listAccountRequests();
	});

});
