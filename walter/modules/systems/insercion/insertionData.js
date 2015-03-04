
var app = angular.module('mainApp');

app.controller('LaboralInsertionDataCtrl', function($scope, $timeout, LaboralInsertion) {

	/**
	 * Agregar cv como base 64
	 */
	$scope.addCv = function($fileContent){
		$scope.model.insertionData.cv = window.btoa($fileContent)
		$scope.model.insertionData.cv = null;
	};


  $scope.loadData = function() {

    LaboralInsertion.findLaboralInsertionData($scope.model.selectedUser,
      function(data) {
        $scope.model.insertionData = data;

        console.log($scope.model.insertionData)
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


});
