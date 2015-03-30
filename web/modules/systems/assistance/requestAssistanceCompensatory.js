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



    //Carga el stock disponible de compensatorios
    $scope.loadCompensatoryStock = function(id) {
        Assistance.getJustificationStock($scope.model.session.user_id, id,
			function(justificationStock){
                $scope.model.compensatory.stock = justificationStock.stock;
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
        if (justification.id == '48773fd7-8502-4079-8ad5-963618abe725') {
            $scope.initialize(justification);
        }
    });

    $scope.initialize = function(justification) {
        $scope.clearSelectionsCompensatory();
        $scope.model.compensatory = {id:justification.id, name: justification.name, stock:0};
        $scope.loadCompensatoryStock(justification.id);
        $scope.model.justification = {id:justification.id,begin:null,end:null};
    }


    // Envio la peticion al servidor
    $scope.save = function() {
        Assistance.requestJustification($scope.model.session.user_id,$scope.model.justification,
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
