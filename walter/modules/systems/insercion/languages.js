var app = angular.module('mainApp');


app.controller('LanguagesLaboralInsertionCtrl', function($scope) {

	$scope.addLanguage = function(){
		$scope.insertionData.languages.push({language:"", level:"basico"});
	}
	
	$scope.deleteLanguage = function($index){
		$scope.insertionData.languages.splice($index, 1);
	}
	

});
