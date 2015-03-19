var app = angular.module('mainApp');

app.controller('RequestAssistanceOutCtrl', function($scope) {
    $scope.isSelectedJustificationOut = function(){
		return $scope.model.justificationOutSelected;
	}

	$scope.selectJustificationOut = function(){
		var value = !$scope.model.justificationOutSelected;
		$scope.clearSelections();
		$scope.model.justificationOutSelected = value;
	}
});
