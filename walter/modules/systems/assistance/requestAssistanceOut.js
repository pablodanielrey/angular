var app = angular.module('mainApp');

app.controller('RequestAssistanceOutCtrl', function($scope) {


    $scope.isSelectedJustificationOut = function(){
		return $scope.model.justificationOutSelected;
	}

	$scope.selectJustificationOut = function(){
		var value = !$scope.model.justificationOutSelected;
		$scope.clearSelections();
        $scope.clearSelectionsOut();
        $scope.model.justification = {};
		$scope.model.justificationOutSelected = value;
	}



    $scope.model.justificationOutRequestSelected = false;
    $scope.model.justificationOutAvailableSelected = false;
    $scope.model.justificationOutRequestsSelected = false;

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
		$scope.clearSelectionsOut();
		$scope.model.justificationOutRequestSelected = true;
	};


	$scope.selectJustificationOutRequests = function(){
		$scope.clearSelectionsOut();
		$scope.model.justificationOutRequestsSelected = true;
	};

	$scope.selectJustificationOutAvailable = function(){
		$scope.clearSelectionsOut();
		$scope.model.justificationOutAvailableSelected = true;

	};


	$scope.clearSelectionsOut = function(){
		$scope.model.justificationOutRequestSelected = false;
		$scope.model.justificationOutAvailableSelected = false;
		$scope.model.justificationOutRequestsSelected = false;

	}

});
