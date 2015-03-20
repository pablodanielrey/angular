var app = angular.module('mainApp');

app.controller('RequestAssistanceCtrl', function($scope, $rootScope, $timeout, $window, Session, Assistance, Profiles) {

	$scope.model = {
		requestedLicences : [], //auxiliar para almacenar los datos de las solicitudes de licencias
		justificationAbsentSelected	: false,
		justificationLaoSelected	: false,
		justificationExamSelected	: false,
		justificationOutSelected	: false,
		justificationCompensatorySelected : false
	};

	/**
	 * Obtener justificaciones del servidor
	 */
	$scope.loadJustifications = function() {
    	Assistance.getJustifications($scope.model.session.user_id,
			function(justifications){
				for(i in justifications){
					var justification = {name:justifications[i].name,id:justifications[i].id}
					$scope.$broadcast('findStockJustification',{justification:justification});
				}

			},
			function(error){
				alert(error);
			}
		);
    }



	/**
	 * Dar formato a las solicitudes de licencia del servidor
	 */
	$scope.formatRequestedLicencesFromServer = function(justificationsFromServer){

	}

	$scope.loadRequestedLicences = function() {
		Assistance.getRequestedLicences($scope.model.session.user_id,
			function(requestedLicences){
				$scope.model.requestedLicences = requestedLicences;

			},
			function(error){
				alert(error);
			}
		);
	}

	/**
	 * cargar datos de la session
	 */
	$scope.initialize = function(){
		$scope.clearSelections();


		$scope.model.session = Session.getCurrentSession();
		if ((!$scope.model.session) || (!$scope.model.session.user_id)) {
			alert("Error: Session no definida");
			$window.location.href = "/#/logout";
        } else {
			Profiles.checkAccess(Session.getSessionId(),'ADMIN-ASSISTANCE,USER-ASSISTANCE',
				function(ok) {
					if (ok == 'granted') {
						console.log("granted");
						$scope.loadJustifications();
						$scope.loadRequestedLicences();
					} else {
						console.log("not granted");
						$window.location.href = "/#/logout";
					}
				},
				function (error) {
					alert(error);
				}
			);
		}
	};


	$scope.clearSelections = function() {
		$scope.model.justificationAbsentSelected = false;
		$scope.model.justificationCompensatorySelected = false;
		$scope.model.justificationExamSelected = false;
		$scope.model.justificationOutSelected = false;
		$scope.model.justificationLaoSelected = false;
	}



    $timeout(function() {
        $scope.initialize();
    }, 0);

});
