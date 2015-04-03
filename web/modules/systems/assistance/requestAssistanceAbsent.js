var app = angular.module('mainApp');

app.controller('RequestAssistanceAbsentCtrl', function($scope, Assistance, Notifications) {

	$scope.model.absent = {
		id:null,
		name:"absent",
		stock:0
	};

	$scope.model.justificationAbsentRequestSelected = false;
	$scope.model.justificationAbsentRequestDateSelected = false; //flag para indicar que se ha definido el dia de la solicitud
	$scope.model.justificationAbsentAvailableSelected = false;
	$scope.model.justificationAbsentRequestsSelected = false;
	$scope.model.requestAbsentBegin = null;
	$scope.model.requestAbsentBeginFormated = null;

	/**
	 * Esta definido el dia de la solicitud?
	 */
	$scope.changeRequestAbsentBegin = function() {
		if($scope.model.requestAbsentBegin != null) {
			$scope.model.justificationAbsentRequestDateSelected = true;
			$scope.model.requestAbsentBeginFormated = $scope.model.requestAbsentBegin.toLocaleDateString();
			return true;
		} else {
			$scope.model.justificationAbsentRequestDateSelected = false;
			$scope.model.requestAbsentBeginFormated = null;
			return false;
		}
	};

	$scope.isSelectedJustificationAbsent = function() {
		return $scope.model.justificationAbsentSelected;
	};

	$scope.isSelectedJustificationAbsentRequestDate = function() {
		return $scope.model.justificationAbsentRequestDateSelected;
	};

	$scope.selectJustificationAbsent = function() {
		var value = !$scope.model.justificationAbsentSelected;
		$scope.clearSelections();
		$scope.model.justificationAbsentSelected = value;

		$scope.model.absent.id = $scope.model.justificationAbsentId;
	};

	$scope.isSelectedJustificationAbsentRequest = function() {
		return $scope.model.justificationAbsentRequestSelected;
	};

	$scope.isSelectedJustificationAbsentAvailable = function() {
		return $scope.model.justificationAbsentAvailableSelected;
	};

	$scope.isSelectedJustificationAbsentRequests = function() {
		return $scope.model.justificationAbsentRequestsSelected;
	};

	$scope.selectJustificationAbsentRequest = function() {
		$scope.clearSelectionsAbsent();
		$scope.model.justificationAbsentRequestSelected = true;
	};


	$scope.selectJustificationAbsentRequests = function() {
		$scope.clearSelectionsAbsent();
		$scope.model.justificationAbsentRequestsSelected = true;
	};

	$scope.selectJustificationAbsentAvailable = function() {
		$scope.clearSelectionsAbsent();
		$scope.model.justificationAbsentAvailableSelected = true;

	};


	$scope.clearSelectionsAbsent = function() {
		$scope.model.justificationAbsentRequestDateSelected = false;
		$scope.model.justificationAbsentRequestSelected = false;
		$scope.model.justificationAbsentAvailableSelected = false;
		$scope.model.justificationAbsentRequestsSelected = false;

	}




	//Carga el stock disponible de los ausentes con aviso
    $scope.loadAbsentStock = function(id) {
        Assistance.getJustificationStock($scope.model.session.user_id, id, null, null,
					function(justificationStock){
						$scope.model.absent.stock = justificationStock.stock;
					},
					function(error){
						alert(error);
					}
				);
				Assistance.getJustificationStock($scope.model.session.user_id, id, null, 'YEAR',
					function(justificationStock){
						$scope.model.absent.yearlyStock = justificationStock.stock;
					},
					function(error){
						alert(error);
					}
				);
    }


    /**
	 * Actualmente solo puede solicitar un dia a la vez
	 */
	$scope.confirmRequestAbsent = function() {

		var requestedJustification = {
			id:$scope.model.absent.id,
			begin:$scope.model.requestAbsentBegin
		}
		Assistance.requestJustification($scope.model.session.user_id, requestedJustification,
			function(ok) {
				$scope.clearSelections();
				Notifications.message('Ausente con aviso solicitado correctamente');
			},
			function(error){
				Notifications.message(error);
			}

		);
	}


	$scope.initialize = function(justification) {
    $scope.model.absent = {id:justification.id, name:justification.name, stock:0};
		$scope.loadAbsentStock(justification.id);
	}

	// Escuchar evento de inicializacion
	$scope.$on('findStockJustification', function(event, data) {
	  justification = data.justification;
	  if (justification.id == $scope.model.justificationAbsentId) {
			$scope.initialize(justification);
	  }
	});

	$scope.$on('JustificationStockChangedEvent', function(event, data) {
		if ($scope.model.justificationAbsentId == data.justification_id) {
			$scope.loadAbsentStock($scope.model.justificationAbsentId);
		}
	});


});
