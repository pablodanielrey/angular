var app = angular.module('mainApp');

app.controller('RequestAssistanceExamCtrl', function($scope) {

    $scope.model.justificationExamRequestSelected = false;
	$scope.model.justificationExamAvailableSelected = false;
	$scope.model.justificationExamRequestsSelected = false;

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
		var value = !$scope.model.justificationExamRequestSelected;
		$scope.clearSelectionsExam();
		$scope.model.justificationExamRequestSelected = value;
	};


	$scope.selectJustificationExamRequests = function(){
		var value = !$scope.model.justificationExamRequestsSelected;
		$scope.clearSelectionsExam();
		$scope.model.justificationExamRequestsSelected = value;
	};

	$scope.selectJustificationExamAvailable = function(){
		var value = !$scope.model.justificationExamAvailableSelected;
		$scope.clearSelectionsExam();
		$scope.model.justificationExamAvailableSelected = value;

	};


	$scope.clearSelectionsExam = function(){
		$scope.model.justificationExamRequestSelected = false;
		$scope.model.justificationExamAvailableSelected = false;
		$scope.model.justificationExamRequestsSelected = false;

	}

});
