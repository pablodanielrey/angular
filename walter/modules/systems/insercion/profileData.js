var app = angular.module('mainApp');


app.controller('ProfileLaboralInsertionCtrl', function($scope,$timeout, Session, Users, Student, LaboralInsertion) {


  $scope.loadData = function() {

    Users.findUser($scope.model.selectedUser,
      function(user) {
        user.birthdate = new Date(user.birthdate);
        $scope.model.userData = user;
      },
      function(error) {
        alert(error);
      }
    );

    Student.findStudentData($scope.model.selectedUser,
      function(data) {
        $scope.model.studentData = data.student;
      },
      function(error) {
        alert(error);
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
