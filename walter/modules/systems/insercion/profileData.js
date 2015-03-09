var app = angular.module('mainApp');

app.controller('ProfileLaboralInsertionCtrl', function($scope,$timeout, Session, Users, Student, LaboralInsertion) {


	$scope.loadData = function() {

		Users.findUser($scope.model.selectedUser,
			function(user) {
				$scope.model.userData = user;
				$scope.formatUser();
			},
			function(error) {
				alert(error);
			}
		);

		Student.findStudentData($scope.model.selectedUser,
			function(student) {
				$scope.model.studentData = student;
			},
			function(error) {
				alert(error);
			}
		);
		

	}
  
	/**
	 * Dar formato a los datos de user para que sean visualizados correctamente a los usuarios
	 */
	$scope.formatUser = function(){
		//fecha de nacimiento
		$scope.model.userData.birthdate = new Date($scope.model.userData.birthdate);
		
		$scope.model.userData.cellPhone = {
			country:"54",
			city:"221",
			number:"123456789",
		};
		
		$scope.model.userData.homePhone = {
			country:"54",
			city:"221",
			number:"123456789",
		};
		
		//telefonos
		if(($scope.model.userData.telephones != undefined) || ($scope.model.userData.telephones != null)){
			for(var telephone in $scope.model.userData.telephones){
				switch($scope.model.userData.telephones[telephone].type){
					case "cell":					
						$scope.model.userData.cellPhone.country = "54";
						$scope.model.userData.cellPhone.city = "221";
						$scope.model.userData.cellPhone.number = "123456789";
					break;
					case "home":
						$scope.model.userData.homePhone.country = "54";
						$scope.model.userData.homePhone.city = "221";
						$scope.model.userData.homePhone.number = "123456789";
					break;
				}
			}
		}
		
		
	};
	
	
	$scope.$on('EditInsertionCheckDataEvent',function(){
		$scope.model.status.profile = true;
		
		$scope.model.userData.telephones = [];
		if($scope.model.userData.cellPhone){
			var telephone = {
				type:"cell",
				number:$scope.model.userData.cellPhone.country + " " + $scope.model.userData.cellPhone.city + " 15 " + $scope.model.userData.cellPhone.number,
			}
			$scope.model.userData.telephones.push(telephone);
		}
		
		if($scope.model.userData.homePhone){
			var telephone = {
				type:"home",
				number:$scope.model.userData.homePhone.country + " " + $scope.model.userData.homePhone.city + " " + $scope.model.userData.homePhone.number,
			}
			$scope.model.userData.telephones.push(telephone);
		}
		
		$scope.$emit("EditInsertionDataCheckedEvent");
		
	});

	$scope.test = function(){
		alert("test");
	};

	$scope.$on('UpdateUserDataEvent',function(event,data) {
		$scope.loadData();
	});


	$timeout(function() {
		$scope.loadData();
	},0);

});
