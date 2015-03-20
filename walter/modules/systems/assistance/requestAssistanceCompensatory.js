var app = angular.module('mainApp');

app.controller('RequestAssistanceCompensatoryCtrl', function($scope, Assistance) {

    $scope.model.justificationCompensatoryRequestSelected = false;
	$scope.model.justificationCompensatoryAvailableSelected = false;
	$scope.model.justificationCompensatoryRequestsSelected = false;

    $scope.isSelectedJustificationCompensatory = function(){
		return $scope.model.justificationCompensatorySelected;
	};

	$scope.selectJustificationCompensatory = function(){
		var value = !$scope.model.justificationCompensatorySelected;
		$scope.clearSelections();
		$scope.model.justificationCompensatorySelected = value;
	};


	$scope.isSelectedJustificationCompensatoryRequest = function(){
		return $scope.model.justificationCompensatoryRequestSelected;
	};

    $scope.isSelectedJustificationCompensatoryAvailable = function(){
		return $scope.model.justificationCompensatoryAvailableSelected;
	};

	$scope.isSelectedJustificationCompensatoryRequests = function(){
		return $scope.model.justificationCompensatoryRequestsSelected;
	};

	$scope.selectJustificationCompensatoryRequest = function(){
		$scope.clearSelectionsCompensatory();
		$scope.model.justificationCompensatoryRequestSelected = true;
	};


	$scope.selectJustificationCompensatoryRequests = function(){
		$scope.clearSelectionsCompensatory();
		$scope.model.justificationCompensatoryRequestsSelected = true;
	};

	$scope.selectJustificationCompensatoryAvailable = function(){
		$scope.clearSelectionsCompensatory();
		$scope.model.justificationCompensatoryAvailableSelected = true;

	};


	$scope.clearSelectionsCompensatory = function(){
		$scope.model.justificationCompensatoryRequestSelected = false;
		$scope.model.justificationCompensatoryAvailableSelected = false;
		$scope.model.justificationCompensatoryRequestsSelected = false;

	}


    // Carga el stock que se puede tomar
    $scope.loadCompensatoryActualStock = function(id) {
        Assistance.getJustificationActualStock($scope.model.session.user_id, id,
			function(justificationActualStock){
				$scope.model.compensatory.actualStock = justificationActualStock;
			},
			function(error){
				alert(error);
			}
		);
    }

    //Carga el stock disponible de compensatorios
    $scope.loadCompensatoryStock = function(id) {
        Assistance.getJustificationStock($scope.model.session.user_id, id,
			function(justificationStock){
                $scope.loadCompensatoryActualStock(id);
				$scope.model.compensatory.stock = justificationStock;
			},
			function(error){
				alert(error);
			}
		);
    }

    // Cargo el stock de la justificacion
    // data.justification = {name,id}
    $scope.$on('findStockJustification', function(event, data) {
        justification = data.justification;
        if (justification.name == 'compensatory') {
            $scope.model.compensatory = {id:justification.id, name:justification.name, stock:0, actualStock:0};
            $scope.loadCompensatoryStock(justification.id);
        }
    });

});
