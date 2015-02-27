var app = angular.module('mainApp');


app.controller('LanguagesLaboralInsertionCtrl', function($scope, $timeout, LaboralInsertion) {

	$scope.addLanguage = function() {
		$scope.languages.push({language:"", level:"básico"});
	}

	$scope.addLanguageIfNone = function(){
		if($scope.languages.length == 0){
			$scope.addLanguage();
		}
	}

	$scope.deleteLanguage = function($index){
		$scope.languages.splice($index, 1);
	}

	$scope.loadData = function() {
		LaboralInsertion.findLanguageData($scope.selectedUser,
			function(data) {
				if ((data != undefined) && (data != null)){
					$scope.languages = data;
				}
				$scope.addLanguageIfNone();
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
