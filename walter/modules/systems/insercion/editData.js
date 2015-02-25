var app = angular.module('mainApp');

app.controller('EditInsertionDataCtrl',function($scope, $timeout, $location, Session, Users, LaboralInsertion) {

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


    $scope.checkTermsAndConditions();


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
  

	/**
	 * procesar verificacion de terminos y condiciones
	 */
	$scope.checkTermsAndConditions = function(){
		console.log("TODO: Actualmente no se esta controlando los terminos y condiciones debido a que no se encuentran implementados en el servidor. Una vez que esten definidos en el servidor la accion checkTermsAndConditions se debe modificar el metodo del controlador editData.checkTermsAndConditions!!!");	 //TODO QUITAR ESTA LINEA UNA VEZ QUE ESTE DEFINIDAS LA ACCION CHECKTERMS AND CONDITION EN EL SERVIDOR Y DESCOMENTAR EL CODIGO
		
		/*
		var session = Session.getCurrentSession(); 
		if((session == null) || (session.selectedUser == null)){
			alert("error: usuario no seleccionado");
			$location.path('/main');			
		} 
		
		/**
		 * callback en el caso de que el servidor haya devuelto una respuesta correcta
		 * @param accepted Booleano que indica si la condicion esta aceptada o no
		 *
		callbackOk = function(response){
			if(!response.accepted){
				$location.path('/acceptTermsAndConditionsInsertion');
			}
		}
		
		/**
		 * callback en el caso de que el servidor haya devuelto una respuesta erronea
		 * @param error String con el error
		 *
		callbackError = function(error){
			console.log(error)
			$location.path('/main');
		}

		LaboralInsertion.isTermsAndConditionsAccepted(session.selectedUser, callbackOk, callbackError);
		*/

	}

	$timeout(function() {
		$scope.checkTermsAndConditions();	
	});


});
