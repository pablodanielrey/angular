var app = angular.module('mainApp');

app.controller('RequestAssistanceCompensatoryCtrl', function($scope, Assistance, Session, Notifications) {

  $scope.model.justificationCompensatoryRequestSelected = false;
	$scope.model.justificationCompensatoryAvailableSelected = false;
	$scope.model.justificationCompensatoryRequestsSelected = false;

  $scope.model.processingRequest = false;

    // ------------------ Manejo de la vista ----------------------------

  $scope.isSelectedJustificationCompensatory = function() {
		return $scope.model.justificationCompensatorySelected;
	};

	$scope.selectJustificationCompensatory = function() {
		var value = !$scope.model.justificationCompensatorySelected;
		$scope.clearSelections();
        $scope.clearSelectionsCompensatory();
		$scope.model.justificationCompensatorySelected = value;

        $scope.model.justification.id = $scope.model.justificationCompensatoryId;
	};


	$scope.isSelectedJustificationCompensatoryRequest = function() {
		return $scope.model.justificationCompensatoryRequestSelected;
	};

    $scope.isSelectedJustificationCompensatoryAvailable = function() {
		return $scope.model.justificationCompensatoryAvailableSelected;
	};

	$scope.isSelectedJustificationCompensatoryRequests = function() {
		return $scope.model.justificationCompensatoryRequestsSelected;
	};

	$scope.selectJustificationCompensatoryRequest = function() {
		$scope.clearSelectionsCompensatory();
		$scope.model.justificationCompensatoryRequestSelected = true;
	};


	$scope.selectJustificationCompensatoryRequests = function() {
		$scope.clearSelectionsCompensatory();
		$scope.model.justificationCompensatoryRequestsSelected = true;
	};

	$scope.selectJustificationCompensatoryAvailable = function() {
		$scope.clearSelectionsCompensatory();
		$scope.model.justificationCompensatoryAvailableSelected = true;

	};


	$scope.clearSelectionsCompensatory = function() {
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
        Assistance.getJustificationStock($scope.model.session.user_id, id, null, null,
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
        if (justification.id == $scope.model.justificationCompensatoryId) {
            $scope.initialize(justification);
        }
    });

    $scope.$on('JustificationStockChangedEvent', function(event, data) {
      if ($scope.model.justificationCompensatoryId == data.justification_id) {
        $scope.loadAbsentStock($scope.model.justificationCompensatoryId);
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
      $scope.model.processingRequest = true;

      Assistance.requestJustification($scope.model.session.user_id,$scope.model.justification,
          function(ok) {
            $scope.model.processingRequest = false;

            Notifications.message("Guardado exitosamente");
            $scope.clearSelections();
          },
          function(error) {
            $scope.model.processingRequest = false;

            Notifications.message(error);
          }
      );
    }


});
