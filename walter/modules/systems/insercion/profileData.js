var app = angular.module('mainApp');


app.controller('ProfileLaboralInsertionCtrl', function($scope,$timeout, Session, Users, Student, LaboralInsertion) {

  $scope.studentData = {};
  $scope.insertionData = {};
  $scope.user = {};

  $scope.$on('SaveEvent',function() {

    var collectedData = { studentData: $scope.studentData, insertionData: $scope.insertionData, $userData: $scope.user };
    var saveData = { type:'profile', data: collectedData };
    $scope.$emit('SaveDataEvent',saveData);

  });

  $scope.clearUserData = function() {
    $scope.user = {};
    $scope.insertionData = {};
  }


  $scope.loadUserData = function() {
    var s = Session.getCurrentSession();
    if (s == null) {
      return;
    }
    if (s.selectedUser == undefined || s.selectedUser == null) {
      $scope.clearUserData();
    }

    var uid = s.selectedUser;

    Users.findUser(uid,
      function(user) {
        user.birthdate = new Date(user.birthdate);
        $scope.user = user;
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

  $timeout($scope.loadUserData());

});
