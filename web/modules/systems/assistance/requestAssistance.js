var app = angular.module('mainApp');

app.controller('RequestAssistanceCtrl', function($scope, $rootScope, $timeout, $window, Session, Assistance, Profiles) {

	$scope.model = {
		justifications : [], //auxiliar para almacenar las justificaciones
		requestedLicences : [], //solicitudes de licencias
		justification : {}, //justificacion a guardar
		justificationAbsentSelected	: false,
		justificationLaoSelected	: false,
		justificationExamSelected	: false,
		justificationOutSelected	: false,
		justificationCompensatorySelected : false,
		justificationCompensatoryId : "48773fd7-8502-4079-8ad5-963618abe725", // id de la justificacion de compensatorio
		justificationOutId : 'fa64fdbd-31b0-42ab-af83-818b3cbecf46' //id de la justificacion de boleta de salidas
	};

	/**
	 * Obtener justificaciones del servidor
	 */
	$scope.loadJustifications = function() {
    	Assistance.getJustifications(
			function(justifications){
				for(i in justifications){
					var justification = {name:justifications[i].name,id:justifications[i].id};
					$scope.$broadcast('findStockJustification',{justification:justification});
					$scope.model.justifications[justifications[i].id] = justifications[i];
				}


			},
			function(error){
				alert(error);
			}
		);
    }


	$scope.formatName = function(name){
		switch(name){
			case "absent":
				return "Ausente con aviso";
			break;
			case "compensatory":
				return "Compensatorio";
			break;
			case "out":
				return "Salida eventual";
			break;
			case "exam":
				return "Pre examen";
			break;
			case "102":
				return "Articulo 102";
			break;
		}
	}

	$scope.loadRequestedLicences = function() {
		Assistance.getJustificationRequests(null,null,
			function(requestedLicences){
				for(i in requestedLicences){
					var requestedLicence = requestedLicences[i]
					var name = $scope.formatName($scope.model.justifications[requestedLicence.justification_id].name);
					requestedLicence.justification_name = name;
					if(requestedLicence.begin != null){
						var date = new Date(requestedLicence.begin);
						requestedLicence.begin = date.toLocaleDateString();
					}
					if(requestedLicence.end != null){
						var date = new Date(requestedLicence.end);
						requestedLicence.end = date.toLocaleDateString();
					}

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
						// $scope.loadRequestedLicences();
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
		$scope.model.justification = {};
	}



    $timeout(function() {
        $scope.initialize();
    }, 0);

});
