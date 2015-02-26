var app = angular.module('mainApp');

app.controller('EditInsertionDataCtrl',function($scope, $timeout, $location, Session, Users, LaboralInsertion) {

  $scope.studentData = {};

  $scope.degrees = [ {} ];
  $scope.languages = [ {} ];

  $scope.insertionData = {};
  $scope.userData = {};
  $scope.selectedUser = null;


  $scope.save = function() {

    // actualizo los datos del perfil.
    Users.updateUser($scope.userData,
      function(ok) {
        // nada
      },
      function(error) {
        alert(error);
      }
    );

    // actualizo los datos básicos de inserción
    LaboralInsertion.updateLaboralInsertionData($scope.insertionData,
      function(ok) {
        // nada
      },
      function(error) {
        alert(error);
      }
    );

    // actualizo la info de las carreras
    LaboralInsertion.updateDegreeData($scope.degrees,
      function(ok) {
        // nada
      },
      function(error) {
        alert(error);
      }
    );

  }


	/**
	 * procesar verificacion de terminos y condiciones
	 */
	$scope.checkTermsAndConditions = function() {

		LaboralInsertion.isTermsAndConditionsAccepted($scope.selectedUser,
      function(response) {
        if(!response.accepted) {
          $location.path('/acceptTermsAndConditionsInsertion');
        }
      },
      function(error) {
        $location.path('/main');
      }
    );

	}

  $scope.setUserSelected = function() {
    // seteo el usuario seleccionado dentro del scope para que lo usen las subvistas facilmente.
    var s = Session.getCurrentSession();
    if (s == null) {
      $location.path('/main');
    }
    if (s.selectedUser == undefined || s.selectedUser == null) {
      $location.path('/main');
    }
    $scope.selectedUser = s.selectedUser;
  }


	$timeout(function() {
    $scope.setUserSelected();
		$scope.checkTermsAndConditions();
    $scope.$broadcast('UpdateUserDataEvent');
	});


});
