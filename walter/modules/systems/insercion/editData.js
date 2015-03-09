var app = angular.module('mainApp');

app.controller('EditInsertionDataCtrl',function($scope, $timeout, $location, Session, Users, Student, LaboralInsertion) {

  $scope.model = {
    insertionData: {},
    degrees: [],
    languages: [],
    userData: {},
    studentData : {},
    selectedUser: null,
    status: {profile:false, languages:false, degrees:false, laboralInsertion:false} //objeto para indicar si los datos de lenguajes estan en condiciones de guardarse, el objeto sera modificado en los subcontroladores
  };

	/**
	 * Al guardar datos se debe disparar un evento de chequeo que sera escuchado por cada subcontrolador
	 */
	$scope.check = function() {
		$scope.$broadcast('EditInsertionCheckDataEvent');
		$scope.save();
	};

	/**
	 * Escuchar evento de finalizacion de chequeo de datos. Los subcontroladores al finalizar el chequeo dispararan el evento de finalizacion de chequeo de datos.
	 */
	$scope.$on('EditInsertionDataCheckedEvent',function() {
		for(var status in $scope.model.status){
			if(!$scope.model.status[status]){
				//alert("Error de datos");
				//return;
			}
			
		}

		$scope.save();
	});
	
	
	$scope.saveUser = function(){
		// actualizo los datos del perfil.
		Users.updateUser($scope.model.userData,
			function(ok) {
			},
			function(error) {
				alert(error);
			}
		);
	
	};
	
	$scope.saveInsertionData = function(){
		$scope.model.insertionData.id = $scope.model.userData.id;
		
		LaboralInsertion.updateLaboralInsertionData($scope.model.insertionData,
			function(ok) {
			},
			function(error) {
				alert(error);
			}
		);
	
	};
	
	$scope.saveLanguages = function(){

		LaboralInsertion.updateLanguageData($scope.model.userData.id, $scope.model.languages,
			function(ok) {
			},
			function(error) {
				alert(error);
			}
		);
	};
	
	/**
	 * Guardar datos de degrees
	 * @protected
	 */
	$scope.saveDegrees = function(){
	
		$scope.transformDegreeData();

		LaboralInsertion.updateDegreeData($scope.model.userData.id, $scope.model.degrees,
			function(ok) {
			},
			function(error) {
				alert(error);
			}
		);
	}

	/**
	 * Transformar datos de degree. La oferta seleccionada se transfora en su correspondiente valor string
	 * @private
	 */
	$scope.transformDegreeData = function() {
		for (var i = 0; i < $scope.model.degrees.length; i++) {
			$scope.model.degrees[i].work_type = '';
			if ($scope.model.degrees[i].offerInternship) {
	
				$scope.model.degrees[i].work_type += 'Internship;';
			}
			if ($scope.model.degrees[i].offerFullTime) {
				$scope.model.degrees[i].work_type += 'FullTime;';
			}
			if ($scope.model.degrees[i].offerYoungProfessionals) {
				$scope.model.degrees[i].work_type += 'YoungProfessionals;';
			}
		}
	}

	
	$scope.save = function() {
		$scope.saveUser	();
		$scope.saveInsertionData();
		$scope.saveLanguages();
		$scope.saveDegrees();
		/*

		NOTAAAAAAA: esta mal hacerlo aca. debería ir en el controlador de degreeeeee.
		lo acomodo aca para hacerlo rapido y probar que todo funcione.

		$scope.transformDegreeData();


		-------------------------------------------------


		// actualizo la info de las carreras
		LaboralInsertion.updateDegreeData($scope.model.degrees,
		function(ok) {
		// nada
		},
		function(error) {
		alert(error);
		}
		); */
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
