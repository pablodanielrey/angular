var app = angular.module('mainApp');

app.controller('RequestAssistanceExamCtrl', function($scope, Assistance, Session, Notifications) {

    $scope.model.justificationExamRequestSelected = false;
	$scope.model.justificationExamAvailableSelected = false;
	$scope.model.justificationExamRequestsSelected = false;
    $scope.model.justification = {};

    // ------------ Manejo de la vista -----------------

    $scope.isSelectedJustificationExam = function(){
		return $scope.model.justificationExamSelected;
	}

	$scope.selectJustificationExam = function(){
		var value = !$scope.model.justificationExamSelected;
		$scope.clearSelections();
		$scope.model.justificationExamSelected = value;
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

        if ($scope.model.justification != null) {
            $scope.model.justification.begin = null;
        }
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

    // Carga el stock que se puede tomar
    $scope.loadExamActualStock = function(id) {
        Assistance.getJustificationActualStock($scope.model.session.user_id, id,
			function(justificationActualStock){
				$scope.model.exam.actualStock = justificationActualStock;
			},
			function(error){
                Notifications.message(error);
			}
		);
    }


    //Carga el stock disponible de compensatorios
    $scope.loadExamStock = function(id) {
        console.log('Load Exam');
        Assistance.getJustificationStock($scope.model.session.user_id, id,
			function(justificationStock) {
                console.log("Stock:"+$scope.model.exam.stock);
                $scope.model.exam.stock = justificationStock;
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
        if (justification.name == 'exam') {
            $scope.initialize(justification);
        }
    });

    $scope.initialize = function(justification) {
        $scope.clearSelectionsExam();
        $scope.model.exam = {id:justification.id, name: justification.name, stock:0, actualStock:0};
        $scope.loadExamStock(justification.id);
        $scope.loadExamActualStock(justification.id);
        $scope.model.justification = {id:justification.id,begin:null,end:null};
    }


    // Envio la peticion al servidor
    $scope.save = function() {

        Assistance.requestLicence($scope.model.user_id,$scope.model.justification,
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
