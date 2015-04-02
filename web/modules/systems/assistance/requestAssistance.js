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
		justificationAbsentId : 'e0dfcef6-98bb-4624-ae6c-960657a9a741', // id de la justificacion de ausente con aviso
		justificationCompensatoryId : "48773fd7-8502-4079-8ad5-963618abe725", // id de la justificacion de compensatorio
		justificationOutId : 'fa64fdbd-31b0-42ab-af83-818b3cbecf46', //id de la justificacion de boleta de salidas
		justificationExamId : 'b70013e3-389a-46d4-8b98-8e4ab75335d0', // id de la justificacion de prexamen
		justificationLaoId : '76bc064a-e8bf-4aa3-9f51-a3c4483a729a' // id de la justificacion de la licencia anual ordinaria
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

				$scope.loadRequestedLicences();

			},
			function(error){
				alert(error);
			}
		);
    }

	$scope.loadRequestedLicences = function() {
		$scope.model.requestedLicences = [];
		Assistance.getJustificationRequests(null,null,
			function(requestedLicences){
				for(i in requestedLicences){
					var requestedLicence = requestedLicences[i]
					var name = $scope.model.justifications[requestedLicence.justification_id].name;
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
						$scope.loadJustifications();
					} else {
						$window.location.href = "/#/logout";
					}
				},
				function (error) {
					alert(error);
				}
			);
		}
	};


	$scope.$on('JustificationsRequestsUpdatedEvent', function(event, data) {
		if ($scope.model.session.user_id == data.user_id) {
			$scope.loadRequestedLicences();
		}
	});

	$scope.$on('JustificationStatusChangedEvent', function(event, data) {
		for (var i = 0; i < $scope.model.requestedLicences.length; i++) {
			if ($scope.model.requestedLicences[i].id == data.request_id) {
				$scope.loadRequestedLicences();
				break;
			}
		}
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
