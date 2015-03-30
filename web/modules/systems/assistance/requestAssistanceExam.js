var app = angular.module('mainApp');

app.controller('RequestAssistanceExamCtrl', function($scope, Assistance, Session, Notifications) {

    $scope.model.justificationExamRequestSelected = false;
	$scope.model.justificationExamAvailableSelected = false;
	$scope.model.justificationExamRequestsSelected = false;

    // ------------ Manejo de la vista -----------------

    $scope.isSelectedJustificationExam = function(){
		return $scope.model.justificationExamSelected;
	}

	$scope.selectJustificationExam = function(){
		var value = !$scope.model.justificationExamSelected;
		$scope.clearSelections();
		$scope.clearSelectionsExam();
		$scope.model.justificationExamSelected = value;

        $scope.model.justification.id = $scope.model.justificationExamId;
	}


	$scope.isSelectedJustificationExamRequest = function(){
		return $scope.model.justificationExamRequestSelected;
	};

    $scope.isSelectedJustificationExamAvailable = function(){
		return $scope.model.justificationExamAvailableSelected;
	};

	$scope.isSelectedJustificationExamRequests = function(){
		return $scope.model.justificationExamRequestsSelected;
	};

	$scope.selectJustificationExamRequest = function(){
		$scope.clearSelectionsExam();
		$scope.model.justificationExamRequestSelected = true;
	};


	$scope.selectJustificationExamRequests = function(){
		$scope.clearSelectionsExam();
		$scope.model.justificationExamRequestsSelected = true;
	};

	$scope.selectJustificationExamAvailable = function(){
		$scope.clearSelectionsExam();
		$scope.model.justificationExamAvailableSelected = true;

	};


	$scope.clearSelectionsExam = function() {
		$scope.model.justificationExamRequestSelected = false;
		$scope.model.justificationExamAvailableSelected = false;
		$scope.model.justificationExamRequestsSelected = false;
	}

    $scope.isSelectedDate = function() {
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
    $scope.loadExamStock = function(id) {
        Assistance.getJustificationStock($scope.model.session.user_id, id,
			function(justificationStock) {
                $scope.model.exam.stock = justificationStock.stock;

			},
			function(error) {
                Notifications.message(error);
			}
		);
    }



    $scope.initialize = function(justification) {
        $scope.clearSelectionsExam();
        $scope.model.exam = {id:justification.id, name: justification.name, stock:0, actualStock:0};
        $scope.loadExamStock(justification.id);
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

 	// Cargo el stock de la justificacion
    // data.justification = {name,id}
    $scope.$on('findStockJustification', function(event, data) {
        justification = data.justification;
        if (justification.id == $scope.model.justificationExamId) {
            $scope.initialize(justification);
        }
    });


});
