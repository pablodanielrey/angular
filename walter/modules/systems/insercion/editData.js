var app = angular.module('mainApp');

app.controller('EditInsertionDataCtrl',function($scope, $timeout, Session, Users, LaboralInsertion) {


  $scope.user = {};

  $scope.degreeData = false;
  $scope.profileData = false;
  $scope.languageData = false;

  $scope.save = function() {
    $scope.degreeData = false;
    $scope.profileData = false;
    $scope.languageData = false;

    $scope.$broadcast('SaveEvent');
  }

  $scope.$on('SaveDataEvent',function(event,data) {
    if (data.type == undefined) {
      return;
    }

    if (data.type == 'degree') {
      $scope.user.degree = data.data;
      $scope.degreeData = true;
    }

    if (data.type == 'profile') {
      $scope.user.profile = data.data;
      $scope.profileData = true;
    }

    if (data.type == 'language') {
      $scope.user.language = data.data;
      $scope.languageData = true;
    }


    if ($scope.degreeData & $scope.profileData & $scope.languageData) {
      // realizo el save.

      Users.updateUser($scope.user,
        function(ok) {
          // nada
        },
        function(error) {
          alert(error);
        }
      );

      LaboralInsertion.updateLaboralInsertionData($scope.user.profile.insertionData,
        function(ok) {
          // nada
        },
        function(error) {
          alert(error);
        }
      );

    }

  });


});
