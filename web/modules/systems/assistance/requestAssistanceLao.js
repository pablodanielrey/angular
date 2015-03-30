var app = angular.module('mainApp');

app.controller('RequestAssistanceLaoCtrl', function($scope, Assistance, Session, Notifications) {

    $scope.model.justificationLaoRequestSelected = false;
	$scope.model.justificationLaoAvailableSelected = false;
	$scope.model.justificationLaoRequestsSelected = false;

    // -------------- Manejo de la vista ---------------

    $scope.isSelectedJustificationLao = function(){
		return $scope.model.justificationLaoSelected;
	}

	$scope.selectJustificationLao = function(){
		var value = !$scope.model.justificationLaoSelected;
		$scope.clearSelections();
		$scope.clearSelectionsLao();
		$scope.model.justificationLaoSelected = value;

        $scope.model.justification.id = $scope.model.justificationLaoId;
	}


	$scope.isSelectedJustificationLaoRequest = function(){
		return $scope.model.justificationLaoRequestSelected;
	};

    $scope.isSelectedJustificationLaoAvailable = function(){
		return $scope.model.justificationLaoAvailableSelected;
	};

	$scope.isSelectedJustificationLaoRequests = function(){
		return $scope.model.justificationLaoRequestsSelected;
	};

	$scope.selectJustificationLaoRequest = function(){
		$scope.clearSelectionsLao();
		$scope.model.justificationLaoRequestSelected = true;
	};


	$scope.selectJustificationLaoRequests = function(){
		$scope.clearSelectionsLao();
		$scope.model.justificationLaoRequestsSelected = true;
	};

	$scope.selectJustificationLaoAvailable = function(){
		$scope.clearSelectionsLao();
		$scope.model.justificationLaoAvailableSelected = true;

	};


	$scope.clearSelectionsLao = function(){
		$scope.model.justificationLaoRequestSelected = false;
		$scope.model.justificationLaoAvailableSelected = false;
		$scope.model.justificationLaoRequestsSelected = false;
	}

    $scope.isSelectedDate = function() {
        if ($scope.model.justification != null && $scope.model.justification.begin != null && $scope.model.justification.end != null) {
            $scope.dateFormated = $scope.model.justification.begin.toLocaleDateString();
            $scope.dateFormated += "-" + $scope.model.justification.end.toLocaleDateString();
            return true;
        } else {
            $scope.dateFormated = null;
            return false;
        }
    }

    // -----------------------------------------------------------------------------------------


    //Carga el stock disponible de compensatorios
    $scope.loadLaoStock = function(id) {
        Assistance.getJustificationStock($scope.model.session.user_id, id,
			function(justificationStock) {
                $scope.model.lao.stock = justificationStock;
			},
			function(error) {
                Notifications.message(error);
			}
		);
    }

    // Cargo el stock de la justificacion
    // data.justification = {name,id}
    $scope.$on('findStockJustification', function(event, data) {

        justification = data.justification;
        if (justification.id == $scope.model.justificationLaoId) {
            $scope.initialize(justification);
        }
    });

    $scope.initialize = function(justification) {
        $scope.clearSelectionsLao();
        $scope.model.lao = {id:justification.id, name: justification.name, stock:0};
        $scope.loadLaoStock(justification.id);
        $scope.model.justification = {id:justification.id,begin:null,end:null};
    }


    // Envio la peticion al servidor
    $scope.save = function() {

        Assistance.requestJustification($scope.model.session.user_id,$scope.model.justification,
            function(ok) {
                Notifications.message("Guardado exitosamente");
                $scope.clearSelections();
            },
            function(error) {
                Notifications.message(error);
            }
        );
    }
});
