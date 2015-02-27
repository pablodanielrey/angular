var app = angular.module('mainApp');


app.controller('LanguagesLaboralInsertionCtrl', function($scope, $timeout, LaboralInsertion) {

	$scope.addLanguage = function() {
		$scope.model.languages.push({language:"", level:"básico"});
	}

	$scope.addLanguageIfNone = function() {
		if ($scope.model.languages.length == 0) {
			$scope.addLanguage();
		}
	}

	$scope.deleteLanguage = function($index) {
		$scope.model.languages.splice($index, 1);
	}

	$scope.loadData = function() {
		LaboralInsertion.findLanguageData($scope.model.selectedUser,
			function(data) {
				if ((data != undefined) && (data != null) && (data.length > 0)){
					$scope.model.languages = data;
				}
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
