var app = angular.module('mainApp');

app.controller('RequestAssistanceLaoCtrl', function($scope) {
    $scope.isSelectedJustificationLao = function(){
		return $scope.model.justificationLaoSelected;
	}

	$scope.selectJustificationLao = function(){
		var value = !$scope.model.justificationLaoSelected;
		$scope.clearSelections();
		$scope.model.justificationLaoSelected = value;
	}
});
