var app = angular.module('mainApp');

app.controller('RequestAssistanceCtrl', function($scope, $rootScope, $timeout, Session, Assistance, Profiles) {

	$scope.model = {
		justifications : [], //auxiliar para almacenar las justificaciones del usuario y su stock asociado
		requestedLicences : [], //auxiliar para almacenar los datos de las solicitudes de licencias
	};

	/**
	 * Dar formato a las jutificaciones del servidor
	 */
	$scope.formatJustificationsFromServer = function(justificationsFromServer){
		for(var i in justificationsFromServer){
			var name = justificationsFromServer[i].name.toLowerCase();
			var stock = justificationsFromServer[i].stock;

			if((name.indexOf("ausente") > -1)|| (name.indexOf("absent") > -1)){
				$scope.model.justificationAbsent = stock;
			} else if((name.indexOf("comp") > -1)){
				$scope.model.justificationCompensatory = stock;
			} else if((name.indexOf("salida") > -1)|| (name.indexOf("out") > -1)){
				$scope.model.justificationOut = stock;
			} else if(name.indexOf("102") > -1){
				$scope.model.justification102 = stock;
			} else if(name.indexOf("lao") > -1){
				$scope.model.justificationLao = stock;
			} else if(name.indexOf("exam") > -1){
				$scope.model.justificationExam = stock;
			}
		}
	};

	/**
	 * Dar formato a las solicitudes de licencia del servidor
	 */
	$scope.formatRequestedLicencesFromServer = function(justificationsFromServer){

	}

	/**
	 * Obtener justificaciones del servidor
	 */
	$scope.loadJustifications = function() {
    	Assistance.getJustifications($scope.model.session.user_id,
			function(justifications){
				for(i in justifications){
					var id = justifications[i].id;
					$scope.model.justifications[id] = {name:justifications[i].name}
					$scope.loadJustificationStock(id);
				}

				$scope.formatJustificationsFromServer($scope.model.justifications);
			},
			function(error){
				alert(error);
			}
		);
    }

    /**
	 * Consultar datos de stock de justificacion
	 */
    $scope.loadJustificationStock = function(justificationId) {
	    Assistance.getJustificationStock($scope.model.session.user_id, justificationId,
			function(justificationStock){
				$scope.model.justifications[justificationId].stock = justificationStock;
			},
			function(error){
				alert(error);
			}
		);
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

	/**
	* verifica si esta seleccionado el item
	*/

	$scope.isSelected = function(item) {
		var isSelected = false;
		switch (item) {
			case 'justificationAbsent': isSelected = $scope.justificationAbsentSelected; break;
			case 'justificationCompensatory': isSelected = $scope.justificationCompensatorySelected; break;
			case 'justificationExam': isSelected = $scope.justificationExamSelected; break;
			case 'justificationOut': isSelected = $scope.justificationOutSelected; break;
			case 'justificationLao': isSelected = $scope.justificationLaoSelected; break;
		}

		return isSelected;
	}

	$scope.justificationAbsentSelected = false;
	$scope.justificationCompensatorySelected = false;
	$scope.justificationExamSelected = false;
	$scope.justificationOutSelected = false;
	$scope.justificationLaoSelected = false;


	$scope.clearSelections = function() {
		$scope.justificationAbsentSelected = false;
		$scope.justificationCompensatorySelected = false;
		$scope.justificationExamSelected = false;
		$scope.justificationOutSelected = false;
		$scope.justificationLaoSelected = false;
	}

	/**
	* Selecciona un item
	*/
	$scope.select = function(item) {
		switch (item) {
			case 'justificationAbsentSelected':
				var value = !$scope.justificationAbsentSelected;
				$scope.clearSelections();
				$scope.justificationAbsentSelected = value;
				break;

			case 'justificationCompensatorySelected':
				var value = !$scope.justificationCompensatorySelected;
				$scope.clearSelections();
				$scope.justificationCompensatorySelected = value;
				break;

			case 'justificationExamSelected':
				var value = !$scope.justificationExamSelected;
				$scope.clearSelections();
				$scope.justificationExamSelected = value;
				break;

			case 'justificationOutSelected':
				var value = !$scope.justificationOutSelected;
				$scope.clearSelections();
				$scope.justificationOutSelected = value;
				break;

			case 'justificationLaoSelected':
				var value = !$scope.justificationLaoSelected;
				$scope.clearSelections();
				$scope.justificationLaoSelected = value;
				break;
		}
	}


    $timeout(function() {
        $scope.initialize();
    }, 0);

});
