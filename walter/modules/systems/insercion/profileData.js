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
		//fecha de nacimiento
	$scope.formatUser = function(){
		$scope.model.userData.birthdate = new Date($scope.model.userData.birthdate);
		
		//telefonos
		if(($scope.model.userData.telephones != undefined) || ($scope.model.userData.telephones != null)){
			for(var telephone in $scope.model.userData.telephones){
				switch($scope.model.userData.telephones[telephone].type){
					case "cell":
						$scope.model.userData.cellPhone = $scope.model.userData.telephones[telephone].number
					break;
					case "home":
						$scope.model.userData.homePhone = $scope.model.userData.telephones[telephone].number
					break;
				}
			}
		}
	};



	$scope.$on('UpdateUserDataEvent',function(event,data) {
		$scope.loadData();
	});


	$timeout(function() {
		$scope.loadData();
	},0);

});
