var app = angular.module('mainApp');

app.controller('RequestAssistanceOutCtrl', function($scope) {

    $scope.model.justificationOutRequestSelected = false;
    $scope.model.justificationOutAvailableSelected = false;
    $scope.model.justificationOutRequestsSelected = false;

    $scope.isSelectedJustificationOut = function(){
		return $scope.model.justificationOutSelected;
	}

	$scope.selectJustificationOut = function(){
		var value = !$scope.model.justificationOutSelected;
		$scope.clearSelections();
		$scope.model.justificationOutSelected = value;
	}


	$scope.isSelectedJustificationOutRequest = function(){
		return $scope.model.justificationOutRequestSelected;
	};

    $scope.isSelectedJustificationOutAvailable = function(){
		return $scope.model.justificationOutAvailableSelected;
	};

	$scope.isSelectedJustificationOutRequests = function(){
		return $scope.model.justificationOutRequestsSelected;
	};

	$scope.selectJustificationOutRequest = function(){
		var value = !$scope.model.justificationOutRequestSelected;
		$scope.clearSelectionsOut();
		$scope.model.justificationOutRequestSelected = value;
	};


	$scope.selectJustificationOutRequests = function(){
		var value = !$scope.model.justificationOutRequestsSelected;
		$scope.clearSelectionsOut();
		$scope.model.justificationOutRequestsSelected = value;
	};

	$scope.selectJustificationOutAvailable = function(){
		var value = !$scope.model.justificationOutAvailableSelected;
		$scope.clearSelectionsOut();
		$scope.model.justificationOutAvailableSelected = value;

	};


	$scope.clearSelectionsOut = function(){
		$scope.model.justificationOutRequestSelected = false;
		$scope.model.justificationOutAvailableSelected = false;
		$scope.model.justificationOutRequestsSelected = false;

	}

});
