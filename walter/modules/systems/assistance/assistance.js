var app = angular.module('mainApp');

app.controller('AssistanceCtrl', function($scope, $timeout, $window, Profiles, Session, Users, Assistance, Notifications) {

	$scope.model = {
		session : null,
		user : {},
    	assistanceStatus : {
    		start : null, //hora de marcacion inicial del dia actual
    		end : null, //hora de marcacion final del dia actual
    		logs : [], //marcaciones iniciales y finales del dia actual
    		workedTime : null//horas trabajadas del dia actual
    	},
    	assistanceData : {
    		position : null, //cargo de la persona
				schedule:[], //fracciones horarias del dia actual
    	},
    	offices : [], //oficinas del usuario
    	justifications : [], //auxiliar para almacenar los datos de las justificaciones
		justificationAbsent : null, //stock de justificaciones ausentes con aviso
		justificationCompensatory : null, //stock de justificaciones compensatorios
		justificationOut : null, //stock de justificaciones salidas eventuales
		justification102 : null, //stock de justificaciones articulo 102
		justificationExam : null, //stock de justificaciones pre examen
		justificationLao : null //stock de justificaciones licencia anual ordinaria
  };

	/**
	 * inicializar datos de usuario
	 */
    $scope.clearUser = function() {
        $scope.model.user = {id:'',name:'',lastname:'',dni:''};
    };

	/**
	 * Dar formato a los datos de oficina recibidos del servidor
	 */
	$scope.formatOfficesFromServer = function(officesFromServer){
		for (var office in officesFromServer){
			$scope.model.offices.push(officesFromServer[office].name);
		}
	};

	/**
	 * Dar formato a los datos del estado de asistencia recibidos del servidor
	 */
	$scope.formatAssistanceStatusFromServer = function(assistanceStatusFromServer){
		$scope.model.assistanceStatus.status = assistanceStatusFromServer.status;

		if (assistanceStatusFromServer.start != null) {
			var start = new Date(assistanceStatusFromServer.start);
			$scope.model.assistanceStatus.start = start.getHours() + ":" + start.getMinutes();
		} else {
			$scope.model.assistanceStatus.start = '00:00';
		}

		if (assistanceStatusFromServer.end != null) {
			var end = new Date(assistanceStatusFromServer.end);
			$scope.model.assistanceStatus.end = end.getHours() + ":" + end.getMinutes();
		} else {
			$scope.model.assistanceStatus.end = '00:00';
		}

		var workedMinutes = assistanceStatusFromServer.workedMinutes;
		var workedH = Math.floor(workedMinutes/60);
		var workedM = workedMinutes % 60;
		$scope.model.assistanceStatus.workedTime = workedH + ":" + workedM;


		for (var i in assistanceStatusFromServer.logs) {
			console.log(assistanceStatusFromServer.logs[i]);
		};

	};

	/**
	 * Dar formato a los datos de asistencia recibidos del servidor
	 */
	$scope.formatAssistanceDataFromServer = function(assistanceDataFromServer){
		$scope.model.assistanceData.position = assistanceDataFromServer.position;

		for (var time in assistanceDataFromServer.schedule) {
			console.log(time);
			var start = new Date(assistanceDataFromServer.schedule[time].start);
			var startHour = start.getHours() + ":" + start.getMinutes();

			var end = new Date(assistanceDataFromServer.schedule[time].end);
			var endHour = end.getHours() + ":" + end.getMinutes()

			$scope.model.assistanceData.schedule.push(startHour + " / " + endHour);
		}
	};

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

	}

	/**
	 * consultar datos de asistencia
	 */
	$scope.loadAssistanceStatus = function(){
		Assistance.getAssistanceStatus($scope.model.session.user_id,
			function(assistanceStatus){
				if(assistanceStatus == undefined){
					Notifications.message('Error al consultar estado');
				} else {
					$scope.formatAssistanceStatusFromServer(assistanceStatus);
				}
			},
			function(error){
				alert(error);
			}
		);
	};

	/**
	 * consultar datos de asistencia
	 */
	$scope.loadAssistanceData = function(){
		Assistance.getAssistanceData($scope.model.session.user_id,
			function(assistanceData){
				$scope.formatAssistanceDataFromServer(assistanceData);
			},
			function(error){
				alert(error);
			}
		);
	};

    $scope.loadUser = function() {
		Users.findUser($scope.model.session.user_id,
			function(user) {
				$scope.model.user = user;
			},
			function(error) {
				alert(error);
			}
		);
    };

    $scope.loadOffices = function() {
    	Assistance.getOfficesByUser($scope.model.session.user_id,
			function(offices){
				$scope.formatOfficesFromServer(offices);
			},
			function(error){
				alert(error);
			}
		);
    }

    $scope.loadJustifications = function() {
    	Assistance.getJustifications(
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


    /**
	 * cargar datos de la session
	 */
	$scope.initialize = function(){
		$scope.model.session = Session.getCurrentSession();
		if ((!$scope.model.session) || (!$scope.model.session.user_id)) {
			alert("Error: Session no definida");
			$window.location.href = "/#/logout";
    } else {
			Profiles.checkAccess(Session.getSessionId(),'ADMIN-ASSISTANCE,USER-ASSISTANCE',
				function(ok) {
					if (ok == 'granted') {
						console.log("granted");
						$scope.loadUser();
						$scope.loadAssistanceStatus();
						$scope.loadAssistanceData();
						$scope.loadOffices();
						$scope.loadJustifications();
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

    $timeout(function() {
		$scope.initialize();
    }, 0);
});
