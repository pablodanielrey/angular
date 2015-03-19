var app = angular.module('mainApp');

app.controller('RequestAssistanceExamCtrl', function($scope) {
    $scope.isSelectedJustificationExam = function(){
		return $scope.model.justificationExamSelected;
	}

	$scope.selectJustificationExam = function(){
		var value = !$scope.model.justificationExamSelected;
		$scope.clearSelections();
		$scope.model.justificationExamSelected = value;
	}
});
