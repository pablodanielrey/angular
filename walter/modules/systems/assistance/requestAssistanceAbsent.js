var app = angular.module('mainApp');

app.controller('RequestAssistanceAbsentCtrl', function($scope) {

	$scope.isSelectedJustificationAbsent = function(){
		return $scope.model.justificationAbsentSelected;
	}
	
	$scope.selectJustificationAbsent = function(){
		var value = !$scope.model.justificationAbsentSelected;
		$scope.clearSelections();
		$scope.model.justificationAbsentSelected = value;
	}
	
});
