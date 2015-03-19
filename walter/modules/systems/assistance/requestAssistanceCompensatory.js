var app = angular.module('mainApp');

app.controller('RequestAssistanceCompensatoryCtrl', function($scope) {

    $scope.isSelectedJustificationCompensatory = function(){
		return $scope.model.justificationCompensatorySelected;
	}

	$scope.selectJustificationCompensatory = function(){
		var value = !$scope.model.justificationCompensatorySelected;
		$scope.clearSelections();
		$scope.model.justificationCompensatorySelected = value;
	}

});
