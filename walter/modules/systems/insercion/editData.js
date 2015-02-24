var app = angular.module('mainApp');

app.controller('EditInsertionDataCtrl',function($scope, $timeout, Session, Users, Student, LaboralInsertion) {

  $scope.user = {};

  $scope.degreeData = false;
  $scope.profileData = false;
  $scope.languageData = false;

  $scope.save = function() {
    $scope.degreeData = false;
    $scope.profileData = false;
    $scope.languageData = false;

    $scope.broadcast('SaveEvent');
  }

  $scope.$on('SaveEventData',function(event,data) {
    if (data.type == undefined) {
      return;
    }

    if (data.type == 'degree') {
      $scope.user.degree = data.data;
    }

    if (data.type == 'profile') {
      $scope.user.profile = data.data;
    }

    if (data.type == 'language') {
      $scope.user.language = data.data;
    }


    if ($scope.degreeData & $scope.profileData & $scope.languageData) {
      // realizo el save.

    }

  });




  /**
  * Carga los datos del usuario seleccionado dentro de la sesion, dentro de la pantalla de datos del perfil.
  */
  $scope.loadUserData = function() {
    var s = Session.getCurrentSession();
    if (s == null) {
      return;
    }
    if (s.selectedUser == undefined || s.selectedUser == null) {
      $scope.clearUser();
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


  $timeout(function() {
    $scope.loadUserData();
  },0);


});
