var app = angular.module('mainApp');


app.controller('ProfileLaboralInsertionCtrl', function($scope,$timeout, Session, Users, Student, LaboralInsertion) {


  $scope.loadData = function() {

    Users.findUser($scope.selectedUser,
      function(user) {
        user.birthdate = new Date(user.birthdate);
        $scope.userData = user;
      },
      function(error) {
        alert(error);
      }
    );

    Student.findStudentData($scope.selectedUser,
      function(data) {
        $scope.studentData = data.student;
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
