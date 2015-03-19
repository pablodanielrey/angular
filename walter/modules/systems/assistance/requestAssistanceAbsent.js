var app = angular.module('mainApp');

app.controller('RequestAssistanceAbsentCtrl', function($scope) {

	$scope.model.justificationAbsentRequestSelected = false;
	$scope.model.justificationAbsentRequestDateSelected = false; //flag para indicar que se ha definido el dia de la solicitud
	$scope.model.justificationAbsentAvailableSelected = false;
	$scope.model.justificationAbsentRequestsSelected = false;
	$scope.model.date = null;

	$scope.changeDate = function(){
		if($scope.model.date != null){
			$scope.model.justificationAbsentRequestDateSelected = true;
		} else {
			$scope.model.justificationAbsentRequestDateSelected = false;
		}
	}

	/**
	 * Esta definido el dia de la solicitud?
	 */
	$scope.isSelectedJustificationAbsentRequestDateSelected = function(){
		return $scope.model.justificationAbsentRequestDateSelected;
	};
					
	$scope.isSelectedJustificationAbsent = function(){
		return $scope.model.justificationAbsentSelected;
	};
	
	$scope.selectJustificationAbsent = function(){
		var value = !$scope.model.justificationAbsentSelected;
		$scope.clearSelections();
		$scope.model.justificationAbsentSelected = value;
	};
		
	$scope.isSelectedJustificationAbsentRequest = function(){
		return $scope.model.justificationAbsentRequestSelected;
	};
	
	$scope.isSelectedJustificationAbsentAvailable = function(){
		return $scope.model.justificationAbsentAvailableSelected;
	};
	
	$scope.isSelectedJustificationAbsentRequests = function(){
		return $scope.model.justificationAbsentRequestsSelected;
	};
	
	$scope.selectJustificationAbsentRequest = function(){
		var value = !$scope.model.justificationAbsentRequestSelected;
		$scope.clearSelectionsAbsent();
		$scope.model.justificationAbsentRequestSelected = value;
		$scope.changeDate();
	};
	
	
	$scope.selectJustificationAbsentRequests = function(){
		var value = !$scope.model.justificationAbsentRequestsSelected;
		$scope.clearSelectionsAbsent();
		$scope.model.justificationAbsentRequestsSelected = value;
	};
	
	$scope.selectJustificationAbsentAvailable = function(){
		var value = !$scope.model.justificationAbsentAvailableSelected;
		$scope.clearSelectionsAbsent();
		$scope.model.justificationAbsentAvailableSelected = value;
		
	};
	
	
	$scope.clearSelectionsAbsent = function(){
		$scope.model.justificationAbsentRequestDateSelected = false;
		$scope.model.justificationAbsentRequestSelected = false;
		$scope.model.justificationAbsentAvailableSelected = false;
		$scope.model.justificationAbsentRequestsSelected = false;
		
	}
	
	
	
});
