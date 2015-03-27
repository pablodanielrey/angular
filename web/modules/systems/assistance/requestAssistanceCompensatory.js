var app = angular.module('mainApp');

app.controller('RequestAssistanceCompensatoryCtrl', function($scope, Assistance, Session, Notifications) {

    $scope.model.justificationCompensatoryRequestSelected = false;
	$scope.model.justificationCompensatoryAvailableSelected = false;
	$scope.model.justificationCompensatoryRequestsSelected = false;
    $scope.model.justification = {};


    // ------------------ Manejo de la vista ----------------------------

    $scope.isSelectedJustificationCompensatory = function(){
		return $scope.model.justificationCompensatorySelected;
	};

	$scope.selectJustificationCompensatory = function(){
		var value = !$scope.model.justificationCompensatorySelected;
		$scope.clearSelections();
        $scope.clearSelectionsCompensatory();
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

        if ($scope.model.justification != null) {
            $scope.model.justification.begin = null;
        }        
	}


    $scope.isSelectedJustificationRequest = function() {
        if ($scope.model.justification != null && $scope.model.justification.begin != null) {
            $scope.dateFormated = $scope.model.justification.begin.toLocaleDateString();
            return true;
        } else {
            $scope.dateFormated = null;
            return false;
        }
    }
    // -----------------------------------------------------------------------------------


    // Carga el stock que se puede tomar
    $scope.loadCompensatoryActualStock = function(id) {
        Assistance.getJustificationActualStock($scope.model.session.user_id, id,
			function(justificationActualStock){
				$scope.model.compensatory.actualStock = justificationActualStock;
			},
			function(error){
                Notifications.message(error);
			}
		);
    }


    //Carga el stock disponible de compensatorios
    $scope.loadCompensatoryStock = function(id) {
        Assistance.getJustificationStock($scope.model.session.user_id, id,
			function(justificationStock){
                $scope.model.compensatory.stock = justificationStock;
			},
			function(error){
                Notifications.message(error);
			}
		);
    }

    // Cargo el stock de la justificacion
    // data.justification = {name,id}
    $scope.$on('findStockJustification', function(event, data) {

        justification = data.justification;
        if (justification.name == 'compensatory') {
            $scope.initialize(justification);
        }
    });

    $scope.initialize = function(justification) {
        $scope.clearSelectionsCompensatory();
        $scope.model.compensatory = {id:justification.id, name: justification.name, stock:0, actualStock:0};
        $scope.loadCompensatoryStock(justification.id);
        $scope.loadCompensatoryActualStock(justification.id);
        $scope.model.justification = {id:justification.id,begin:null,end:null};
    }


    // Envio la peticion al servidor
    $scope.save = function() {

        Assistance.requestJustification($scope.model.user_id,$scope.model.justification,
            function(ok) {
                Notifications.message("Guardado exitosamente");
                $scope.model.justification.begin = null;
                $scope.clearSelections();
            },
            function(error) {
                Notifications.message(error);
            }
        );
    }


});
