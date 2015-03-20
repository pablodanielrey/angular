var app = angular.module('mainApp');

app.controller('RequestAssistanceCtrl', function($scope, $rootScope, $timeout, $window, Session, Assistance, Profiles) {

	$scope.model = {
		justifications : [], //auxiliar para almacenar las justificaciones
		requestedLicences : [], //solicitudes de licencias
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
					$scope.model.justifications[justifications[i].id] = justifications[i];
				}
				

			},
			function(error){
				alert(error);
			}
		);
    }


	$scope.loadRequestedLicences = function() {
		Assistance.getRequestedLicences($scope.model.session.user_id,
			function(requestedLicences){
				for(i in requestedLicences){
					var requestedLicence = requestedLicences[i]
					var name = $scope.model.justifications[requestedLicence.justification_id].name;
					requestedLicence.justification_name = name;
					$scope.model.requestedLicences.push(requestedLicence)
				}

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


	// Escuchar evento de nuevo requerimiento de licencia
	$scope.$on('requestLicenceEvent', function() {
		$scope.loadRequestedLicences();
	});

	
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
