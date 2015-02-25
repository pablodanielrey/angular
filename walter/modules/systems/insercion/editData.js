var app = angular.module('mainApp');

app.controller('EditInsertionDataCtrl',function($scope, $timeout, $location, Session, Users, LaboralInsertion) {

  $scope.studentData = {};
  $scope.insertionData = {};
  $scope.userData = {};

  $scope.$watch("userData",function() {
    console.log('user cambiado');
  });

  $scope.$watch("insertionData",function() {
    console.log('insertion cambiado');
  });

/*
  $scope.degreeData = false;
  $scope.profileData = false;
  $scope.languageData = false;
*/
  $scope.save = function() {
/*
    $scope.degreeData = false;
    $scope.profileData = false;
    $scope.languageData = false;

    $scope.$broadcast('SaveEvent');
*/
    Users.updateUser($scope.userData,
      function(ok) {
        // nada
      },
      function(error) {
        alert(error);
      }
    );

    LaboralInsertion.updateLaboralInsertionData($scope.insertionData,
      function(ok) {
        // nada
      },
      function(error) {
        alert(error);
      }
    );

  }

/*
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
*/

	/**
	 * procesar verificacion de terminos y condiciones
	 */
	$scope.checkTermsAndConditions = function(){
		var session = Session.getCurrentSession();
		if((session == null) || (session.selectedUser == null)){
			alert("error: usuario no seleccionado");
			$location.path('/main');
		}

		/**
		 * callback en el caso de que el servidor haya devuelto una respuesta correcta
		 * @param accepted Booleano que indica si la condicion esta aceptada o no
		 */
		callbackOk = function(response){
			if(!response.accepted){
				$location.path('/acceptTermsAndConditionsInsertion');
			}
		}

		/**
		 * callback en el caso de que el servidor haya devuelto una respuesta erronea
		 * @param error String con el error
		 */
		callbackError = function(error){
			console.log(error)
			$location.path('/main');
		}

		LaboralInsertion.isTermsAndConditionsAccepted(session.selectedUser, callbackOk, callbackError);

	}

	$timeout(function() {
		$scope.checkTermsAndConditions();
	});


});
