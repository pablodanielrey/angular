var app = angular.module('mainApp');


app.controller('LanguagesLaboralInsertionCtrl', function($scope, $timeout, LaboralInsertion) {

	$scope.addLanguage = function() {
		//$scope.insertionData.languages.push({language:"", level:"basico"});
	}

	$scope.deleteLanguage = function($index){
		$scope.languages.splice($index, 1);
	}

	$scope.loadData = function() {
		LaboralInsertion.findLaboralInsertionData($scope.selectedUser,
			function(data) {
				$scope.languages = data;
			},
			function(err) {
				alert(err);
			}
		);
	}

	$scope.$on('UpdateUserDataEvent',function(event,data) {
		$scope.loadData();
	});

	$timeout(function() {
		$scope.loadData();
	},0);

});
