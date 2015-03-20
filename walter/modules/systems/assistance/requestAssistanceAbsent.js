var app = angular.module('mainApp');

app.controller('RequestAssistanceAbsentCtrl', function($scope, Assistance, Notifications) {


	$scope.model.absent = {
		id:null,
		name:"absent",
		stock:0,
		actualStock:0
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
	$scope.isSelectedJustificationAbsentRequestDateSelected = function(){
		if($scope.isSelectedJustificationAbsentRequest()){
			if($scope.model.requestAbsentBegin != null){
				if($scope.model.requestAbsentBeginFormated != $scope.model.requestAbsentBegin.toLocaleDateString()){
					$scope.model.requestAbsentBeginFormated = $scope.model.requestAbsentBegin.toLocaleDateString();
				}
				return true;
			} else {
				$scope.model.requestAbsentBeginFormated = null;
			}
		}
	
		return false;
	};
					
	$scope.isSelectedJustificationAbsent = function(){
		return $scope.model.justificationAbsentSelected;
	};
	
	$scope.selectJustificationAbsent = function(){
		var value = !$scope.model.justificationAbsentSelected;
		$scope.clearSelections();
		$scope.model.justificationAbsentSelected = value;
	};
		
	$scope.isSelectedJustificationAbsentRequest = function(){
		return $scope.model.justificationAbsentRequestSelected;
	};
	
	$scope.isSelectedJustificationAbsentAvailable = function(){
		return $scope.model.justificationAbsentAvailableSelected;
	};
	
	$scope.isSelectedJustificationAbsentRequests = function(){
		return $scope.model.justificationAbsentRequestsSelected;
	};
	
	$scope.selectJustificationAbsentRequest = function(){
		var value = !$scope.model.justificationAbsentRequestSelected;
		$scope.clearSelectionsAbsent();
		$scope.model.justificationAbsentRequestSelected = value;
	};
	
	
	$scope.selectJustificationAbsentRequests = function(){
		var value = !$scope.model.justificationAbsentRequestsSelected;
		$scope.clearSelectionsAbsent();
		$scope.model.justificationAbsentRequestsSelected = value;
	};
	
	$scope.selectJustificationAbsentAvailable = function(){
		var value = !$scope.model.justificationAbsentAvailableSelected;
		$scope.clearSelectionsAbsent();
		$scope.model.justificationAbsentAvailableSelected = value;
		
	};
	
	
	$scope.clearSelectionsAbsent = function(){
		$scope.model.justificationAbsentRequestDateSelected = false;
		$scope.model.justificationAbsentRequestSelected = false;
		$scope.model.justificationAbsentAvailableSelected = false;
		$scope.model.justificationAbsentRequestsSelected = false;
		
	}
	
	
	
	 // Carga el stock que se puede tomar
    $scope.loadAbsentActualStock = function(id) {
        Assistance.getJustificationActualStock($scope.model.session.user_id, id,
			function(justificationActualStock){
				$scope.model.absent.actualStock = justificationActualStock;
			},
			function(error){
				alert(error);
			}
		);
    }
    
	//Carga el stock disponible de los ausentes con aviso
    $scope.loadAbsentStock = function(id) {
        Assistance.getJustificationStock($scope.model.session.user_id, id,
			function(justificationStock){
				$scope.model.absent.stock = justificationStock;
			},
			function(error){
				alert(error);
			}
		);
    }
    
    
    /**
	 * Actualmente solo puede solicitar un dia a la vez
	 */
	$scope.confirmRequestAbsent = function(){
	
		var requestLicence = {
			id:$scope.model.absent.id,
			start:$scope.model.absentStart, 
			end:$scope.model.absentStart, 
		}
		Assistance.requestLicence($scope.model.session.user_id, requestLicence,
			function(ok){
				$scope.model.requestAbsentBegin = null;
				$scope.selectJustificationAbsentRequests();
				Notifications.message('Ausente con aviso solicitado correctamente');
			},
			function(error){
				alert(error);
			}
		
		);
	}
	
	
	$scope.initialize = function(justification){
        $scope.model.absent = {id:justification.id, name:justification.name, stock:0, actualStock:0};
		$scope.loadAbsentStock(justification.id);
		$scope.loadAbsentActualStock(justification.id);	
	}

	// Escuchar evento de inicializacion
    $scope.$on('findStockJustification', function(event, data) {
    
        justification = data.justification;
        if (justification.name == 'absent') {
			$scope.initialize(justification);
        }
        
    });
	
});
