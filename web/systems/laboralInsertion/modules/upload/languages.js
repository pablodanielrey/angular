var app = angular.module('mainApp');


app.controller('LanguagesLaboralInsertionCtrl', function($scope, $timeout, LaboralInsertion) {

	$scope.addLanguage = function() {
		$scope.model.languages.push({ name:"", level:"básico" });
	}

	$scope.addLanguageIfNone = function() {
		if ($scope.model.languages.length == 0) {
			$scope.addLanguage();
		}
	}

	$scope.deleteLanguage = function($index) {
		$scope.model.languages.splice($index, 1);
		$scope.addLanguageIfNone()
	}


	$scope.$on('EditInsertionCheckDataEvent',function() {
		$scope.model.status.languages = true;

		$scope.$emit("EditInsertionDataCheckedEvent");

	});

});
