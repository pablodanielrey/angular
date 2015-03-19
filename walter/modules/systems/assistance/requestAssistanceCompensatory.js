var app = angular.module('mainApp');

app.controller('RequestAssistanceCompensatoryCtrl', function($scope) {

    $scope.model.justificationCompensatoryRequestSelected = false;
	$scope.model.justificationCompensatoryAvailableSelected = false;
	$scope.model.justificationCompensatoryRequestsSelected = false;

    $scope.isSelectedJustificationCompensatory = function(){
		return $scope.model.justificationCompensatorySelected;
	};

	$scope.selectJustificationCompensatory = function(){
		var value = !$scope.model.justificationCompensatorySelected;
		$scope.clearSelections();
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
		var value = !$scope.model.justificationCompensatoryRequestSelected;
		$scope.clearSelectionsCompensatory();
		$scope.model.justificationCompensatoryRequestSelected = value;
	};


	$scope.selectJustificationCompensatoryRequests = function(){
		var value = !$scope.model.justificationCompensatoryRequestsSelected;
		$scope.clearSelectionsCompensatory();
		$scope.model.justificationCompensatoryRequestsSelected = value;
	};

	$scope.selectJustificationCompensatoryAvailable = function(){
		var value = !$scope.model.justificationCompensatoryAvailableSelected;
		$scope.clearSelectionsCompensatory();
		$scope.model.justificationCompensatoryAvailableSelected = value;

	};


	$scope.clearSelectionsCompensatory = function(){
		$scope.model.justificationCompensatoryRequestSelected = false;
		$scope.model.justificationCompensatoryAvailableSelected = false;
		$scope.model.justificationCompensatoryRequestsSelected = false;

	}

});
