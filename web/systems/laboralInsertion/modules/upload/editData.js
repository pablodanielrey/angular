var app = angular.module('mainApp');

app.controller('EditInsertionDataCtrl',function($rootScope, $scope, Login, LaboralInsertion, Notifications, Utils) {

	$scope.model = {
		insertionData: {},
		degrees: [],
		languages: [],
		userData: {},
		studentData : {}
	};

	$scope.transformations = [];





	/**
	 * Transformar datos de profile
	 */
	$scope.transformProfileData = function(){


		$scope.model.userData.telephones = [];

		if($scope.model.userData.cellPhone && $scope.model.userData.cellPhone.number != "") {
			var telephone = {
				type:"cell",
				number:$scope.model.userData.cellPhone.country + " " + $scope.model.userData.cellPhone.city + " 15 " + $scope.model.userData.cellPhone.number,
			};
			$scope.model.userData.telephones.push(telephone);
		}

		if($scope.model.userData.homePhone && $scope.model.userData.homePhone.number != "") {
			var telephone = {
				type:"home",
				number:$scope.model.userData.homePhone.country + " " + $scope.model.userData.homePhone.city + " " + $scope.model.userData.homePhone.number,
			};
			$scope.model.userData.telephones.push(telephone);
		}
	};


	/**
	 * Transformar datos de insercion
	 */
	$scope.transformInsertionData = function(){

		if($scope.model.insertionData.travel === ""){
			$scope.model.insertionData.travel = false;
		}
		if($scope.model.insertionData.reside === ""){
			$scope.model.insertionData.reside = false;
		}

		if($scope.model.insertionData.cv === ""){
			Notifications.message('Debe cargar CV');
		}
	};


	$scope.save = function() {

		for (var i; i <= $scope.transformations.length; i++) {
			$scope.transformations[i]();
		}

		var data = {
			insertionData: $scope.model.insertionData,
			degrees: $scope.model.degrees,
			languages: $scope.model.languages,
			userData: $scope.model.userData,
			studentData : $scope.model.studentData
		}
		LaboralInsertion.update(data,
			function(ok) {
				if (ok) {
					Notifications.message('Datos actualizados correctamente');
				} else {
					Notifications.message('Error actualizando datos');
				}
			},
			function(err) {
				Notifications.message(err);
			});

	};



	/**
	 * procesar verificacion de terminos y condiciones
	 */
	 /*
	$scope.checkTermsAndConditions = function() {

		LaboralInsertion.isTermsAndConditionsAccepted($scope.model.selectedUser,
			function(response) {
				if(!response.accepted) {
					$location.path('/acceptTermsAndConditionsInsertion');
				}
			},
			function(error) {
				$location.path('/main');
			}
		);

	};
	*/

	$scope.loadData = function() {
		var userId = Login.getUserId();
		LaboralInsertion.find(userId,
			function(data) {
				console.log(data);
				$scope.$emit('UpdateLaboralInsertionDataEvent');
			},
			function(err) {
				Notifications.message(err);
			}
		)
	}


	$scope.initialize = function() {
		$scope.loadData();
	};


	$scope.$on('$viewContentLoaded', function(event) {
		$scope.initialize();
	});

});
