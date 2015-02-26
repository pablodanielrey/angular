var app = angular.module('mainApp');


app.controller('LanguagesLaboralInsertionCtrl', ["$scope", "$timeout", function($scope, $timeout) {
	
	$scope.initializeLanguage = function(){
		if(($scope.insertionData.languages == null) || ($scope.insertionData.languages == undefined)){
			$scope.insertionData.languages = [];
		}
		
		if($scope.insertionData.languages.length == 0){
			$scope.addLanguage();
		}
	}

	$scope.addLanguage = function(){
		$scope.insertionData.languages.push({language:"", level:"basico"});
	}
	
	$scope.deleteLanguage = function($index){
		$scope.insertionData.languages.splice($index, 1);
		$scope.initializeLanguage();
	}
	
	$timeout(function() {
		$scope.initializeLanguage()
	},0);

}]);
