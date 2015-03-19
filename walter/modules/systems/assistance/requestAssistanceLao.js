var app = angular.module('mainApp');

app.controller('RequestAssistanceLaoCtrl', function($scope) {

    $scope.model.justificationLaoRequestSelected = false;
	$scope.model.justificationLaoAvailableSelected = false;
	$scope.model.justificationLaoRequestsSelected = false;

    $scope.isSelectedJustificationLao = function(){
		return $scope.model.justificationLaoSelected;
	}

	$scope.selectJustificationLao = function(){
		var value = !$scope.model.justificationLaoSelected;
		$scope.clearSelections();
		$scope.model.justificationLaoSelected = value;
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
		var value = !$scope.model.justificationLaoRequestSelected;
		$scope.clearSelectionsLao();
		$scope.model.justificationLaoRequestSelected = value;
	};


	$scope.selectJustificationLaoRequests = function(){
		var value = !$scope.model.justificationLaoRequestsSelected;
		$scope.clearSelectionsLao();
		$scope.model.justificationLaoRequestsSelected = value;
	};

	$scope.selectJustificationLaoAvailable = function(){
		var value = !$scope.model.justificationLaoAvailableSelected;
		$scope.clearSelectionsLao();
		$scope.model.justificationLaoAvailableSelected = value;

	};


	$scope.clearSelectionsLao = function(){
		$scope.model.justificationLaoRequestSelected = false;
		$scope.model.justificationLaoAvailableSelected = false;
		$scope.model.justificationLaoRequestsSelected = false;

	}
});
