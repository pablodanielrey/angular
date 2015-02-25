var app = angular.module('mainApp');


app.controller('ProfileLaboralInsertionCtrl', function($scope,$timeout, Session, Users, Student, LaboralInsertion) {


  $scope.$on('SaveEvent',function() {

    var collectedData = { studentData: $scope.studentData, insertionData: $scope.insertionData, $userData: $scope.user };
    var saveData = { type:'profile', data: collectedData };
    $scope.$emit('SaveDataEvent',saveData);

  });

/*
  $scope.clearUserData = function() {
    $scope.userData = {};
    $scope.insertionData = {};
  }
*/

  $scope.loadUserData = function() {

    var s = Session.getCurrentSession();
    if (s == null) {
      return;
    }
    if (s.selectedUser == undefined || s.selectedUser == null) {
      return;
    }

    var uid = s.selectedUser;

    Users.findUser(uid,
      function(user) {
        user.birthdate = new Date(user.birthdate);
        $scope.userData = user;
      },
      function(error) {
        alert(error);
      }
    );

    Student.findStudentData(uid,
      function(data) {
        $scope.studentData = data.student;
      },
      function(error) {
        alert(error);
      }
    );

    LaboralInsertion.findLaboralInsertionData(uid,
      function(data) {
        $scope.insertionData = data;
      },
      function(error) {
        alert(error);
      }
    );
  }

	$timeout(function() {
		$scope.loadUserData();
	},0);

});
