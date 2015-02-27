var app = angular.module('mainApp');

app.controller('EditInsertionDataCtrl',function($scope, $timeout, $location, Session, Users, LaboralInsertion) {

  $scope.model = {
    insertionData: {},
    degrees: [],
    languages: [],
    userData: {},
    selectedUser: null,
    status: {languages:false, degrees:false, laboralInsertion:false} //objeto para indicar si los datos de lenguajes estan en condiciones de guardarse, el objeto sera modificado en los subcontroladores
  };

	/**
	 * Al guardar datos se debe disparar un evento de chequeo que sera escuchado por cada subcontrolador
	 */
	$scope.save = function() {
		$scope.$broadcast('LaboralInsertionCheckDataEvent');
	}
  
	/**
	 * Escuchar evento de finalizacion de chequeo de datos. Los subcontroladores al finalizar el chequeo dispararan el evento de finalizacion de chequeo de datos.
	 */
	$scope.$on('LaboralInsertionDataCheckedEvent',function() {
		for(var status in $scope.model.status){
			if($scope.model.status[status]){
				return;
			}
		}
		
		$scope.mainSave();
	});
	
  $scope.mainSave = function() {

    // actualizo los datos del perfil.
    Users.updateUser($scope.model.userData,
      function(ok) {
        // nada
      },
      function(error) {
        alert(error);
      }
    );

    // actualizo los datos básicos de inserción
    LaboralInsertion.updateLaboralInsertionData($scope.model.insertionData,
      function(ok) {
        // nada
      },
      function(error) {
        alert(error);
      }
    );

    // actualizo la info de las carreras
    LaboralInsertion.updateDegreeData($scope.model.degrees,
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
    $scope.model.selectedUser = s.selectedUser;
  }


	$timeout(function() {
    $scope.setUserSelected();
		$scope.checkTermsAndConditions();
    $scope.$broadcast('UpdateUserDataEvent');
	});


});
