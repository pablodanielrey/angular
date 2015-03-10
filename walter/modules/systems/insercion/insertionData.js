
var app = angular.module('mainApp');

app.controller('LaboralInsertionDataCtrl', function($scope, $timeout, LaboralInsertion) {

	/**
	 * Agregar cv como base 64
	 */
	$scope.addCv = function($fileContent){
		$scope.model.insertionData.cv = window.btoa($fileContent)
	};


  $scope.loadData = function() {

    LaboralInsertion.findLaboralInsertionData($scope.model.selectedUser,
      function(data) {
        $scope.model.insertionData = data;
      },
      function(err) {
        alert(err);
      });

  }

  $scope.$on('UpdateUserDataEvent',function(event,data) {
    $scope.loadData();
  });


  $timeout(function() {
    $scope.loadData();
  });


	/**
	 * chequeo de datos, por el momento se realiza en el editData
	 *
	$scope.$on('EditInsertionCheckDataEvent',function() {
		$scope.model.status.insertion = true;
		
		if($scope.model.insertionData.travel === ""){
			$scope.model.insertionData.travelError = true;
			$scope.model.status.insertion = false;
			alert($scope.model.status.insertion);
		 	$scope.$emit("EditInsertionDataCheckedEvent");

		
		}
		if($scope.model.insertionData.reside === ""){
			$scope.model.insertionData.resideError = true;
			$scope.model.status.insertion = false;
		 	$scope.$emit("EditInsertionDataCheckedEvent");

		}

		
	});
*/
});
