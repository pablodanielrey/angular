var app = angular.module('mainApp');

app.controller('RequestAssistanceCtrl', ["$scope", "$rootScope", "$timeout", "$window", "Session", "Assistance", "Profiles", "Notifications", "Utils", function($scope, $rootScope, $timeout, $window, Session, Assistance, Profiles, Notifications, Utils) {

	$scope.model = {
		justifications : [], //auxiliar para almacenar las justificaciones que seran mostradas al usuario
		requestedLicences : [], //solicitudes de licencias
		justification : {}, //justificacion a guardar OBSOLETO, las justificaciones a guardar deben definirse en cada subcontrolador!!!
		justificationAbsentSelected	: false,
		justificationLaoSelected	: false,
		justificationExamSelected	: false,
		justificationOutSelected	: false,
		justificationCompensatorySelected : false,
    justification102Selected : false,
    justificationBirthdaySelected : false,
    justification638Selected : false,

		justificationAbsentId : "e0dfcef6-98bb-4624-ae6c-960657a9a741", // id de ausente con aviso
		justificationCompensatoryId : "48773fd7-8502-4079-8ad5-963618abe725", // id de la justificacion de compensatorio
		justificationOutId : 'fa64fdbd-31b0-42ab-af83-818b3cbecf46', //id de la justificacion de boleta de salidas
		justificationLaoId : '76bc064a-e8bf-4aa3-9f51-a3c4483a729a' // id de la justificacion de la licencia anual ordinaria
	};

	/**
	 * Obtener justificaciones del servidor
	 */
	$scope.loadJustifications = function() {
    	Assistance.getJustifications(
				function(justifications) {
					for (var i = 0; i < justifications.length; i++) {
						var justification = {
							name: justifications[i].name,
							id: justifications[i].id
						};
						$scope.$broadcast('findStockJustification',{ justification: justification });
						$scope.model.justifications[justifications[i].id] = justifications[i];
					}
					$scope.loadRequestedLicences();

				},
				function(error){
					Notifications.message(error);
				}
			);
    }

	$scope.loadRequestedLicences = function() {
		Assistance.getJustificationRequests(null,
			function(requestedLicences) {
				requestedLicences.sort(function(l1,l2) {
					return (new Date(l1.begin) - (new Date(l2.begin)));
				});

				$scope.model.requestedLicences = [];
				for (var i = 0; i < requestedLicences.length; i++) {
					var req = Utils.formatRequestJustification(requestedLicences[i]);
					$scope.model.requestedLicences.push(req);
				}
			},
			function(error){
				Notifications.message(error);
			}
		);
	};



	/**
		Cancela el pedido de una justificación.
		Solo lo puede hacer el usuario y cuando la justificación esta en el estado de PENDING.
	*/
	$scope.cancelRequest = function(req) {
		Assistance.updateJustificationRequestStatus(req['id'],'CANCELED',
			function(ok) {
				// nada
			},
			function(error) {
				Notifications.message(error);
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
					Notifications.message(error);
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
    $scope.model.justification102Selected = false;
    $scope.model.justification638Selected = false;
    $scope.model.justificationBirthdaySelected = false;
		$scope.model.justification = {};
	}



    $timeout(function() {
        $scope.initialize();
    }, 0);

}]);
