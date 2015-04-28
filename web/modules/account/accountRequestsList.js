
app.controller("AccountRequestsListCtrl", function($rootScope, $scope, Utils, Account, Session) {

	//inicializar filtro
	$scope.filterconfirmed = [];
	$scope.filterconfirmed.confirmed = true;
	$scope.filterconfirmed.unconfirmed = true;
	$scope.filterDescription = [];
	$scope.filterDescriptionSelected = null;


	//inicializo los elementos seleccionados
	$scope.requests = [];
	$scope.accountRequestSelected = [];


	$scope.$on('AccountRequestCreatedEvent', function(event,data) {
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
		$scope.listAccountRequests();
	});

	/**
	 * Seleccionar un requerimiento de cuenta para su edicion, denegacion o aprobacion
	 * @param accountRequestId
	 *
	 */
	$scope.selectAccountRequest = function(accountRequest) {

		var s = Session.getCurrentSession();
		var requests = [];

		if (accountRequest == null) {
			s.accountRequestSelected = null;
			$scope.accountRequestSelected = [];
		} else {
			accountRequest.checked = !accountRequest.checked;
			if (accountRequest.checked) {
				$scope.accountRequestSelected.push(accountRequest);
				request = accountRequest.request;
			} else {
				var index = $scope.accountRequestSelected.indexOf(accountRequest);
				$scope.accountRequestSelected.splice(index, 1);
			}


			for (var i=0; i<$scope.accountRequestSelected.length; i++) {
				requests.push($scope.accountRequestSelected[i].request);
			}
			s.accountRequestSelected = requests;
		}

		Session.saveSession(s);

		$rootScope.$broadcast('AccountRequestSelection',requests);
	};


	$scope.isSelected = function(r) {
		for (var i = 0; i < $scope.accountRequestSelected.length; i++) {
			if ($scope.accountRequestSelected[i] == r) {
				return true;
			}
		}
		return false;
	}

	/**
	 * Definir lista de requerimientos de cuenta
	 *
	 */
	$scope.listAccountRequests = function() {
		Account.listAccounts(
			function(response) {
				$scope.requests = [];
				if (response == undefined) {
					return;
				}
				for (var i = 0; i < response.length; i++) {
					$scope.requests.push({request:response[i],checked:false});
				}
				$scope.loadFilterDescription();
			},
			function(error) {
				$scope.requests = [];
				alert(error);
			});
	};


	/**
	* ---------------------------------------
	*	Filtro de cuentas por la descripcion
	* ---------------------------------------
	**/

	$scope.loadFilterDescription = function() {
		$scope.filterDescription = [];
		$scope.addFilterDescription(null);
		for (var i = 0; i < $scope.requests.length; i++) {
			var r = $scope.requests[i];
			//$scope.addFilterDescription(r);
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
			if (d.label == r.request.reason) {
				d.items.push(r);
				return;
			}
		}
		var desciption = {label:r.request.reason,items:[r],value:r.request.reason};
		$scope.filterDescription.push(desciption);
	}

	$scope.onChangeFilterDescription = function(selected) {
		$scope.requests = selected.items;

		$scope.clearSelectedAccountRequest();
	}

	$scope.clearSelectedAccountRequest = function() {
		$scope.accountRequestSelected = [];
		for (var i=0; i<$scope.requests.length; i++) {
			$scope.requests[i].checked = false;
		}
		$scope.selectAccountRequest(null);
	}

	$scope.$on('InitializeAccountRequestList', function() {
		//llamar a la lista de AccountRequests
		$scope.listAccountRequests();
	});

});
