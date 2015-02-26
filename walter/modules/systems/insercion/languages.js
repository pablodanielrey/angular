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
		LaboralInsertion.findLaboralInsertionData($scope.selectedUser,
			function(data) {
				if((data.laboralInsertion == undefined) || (data.laboralInsertion == null)
				|| (data.laboralInsertion.languages == undefined) || (data.laboralInsertion.languages == null)){

				} else {
					$scope.languages = data.laboralInsertion.languajes;
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
