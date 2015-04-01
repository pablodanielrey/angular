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
		for (var office in officesFromServer.offices){
			$scope.model.offices.push(officesFromServer.offices[office].name);
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
		var workedM = Math.floor(workedMinutes % 60);
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
				Notifications.message(error);
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
				Notifications.message(error);
			}
		);
	};

    $scope.loadUser = function() {
		Users.findUser($scope.model.session.user_id,
			function(user) {
				$scope.model.user = user;
			},
			function(error) {
				Notifications.message(error);
			}
		);
    };

    $scope.loadOffices = function() {
    	Assistance.getOfficesByUser($scope.model.session.user_id,
			function(offices){
				$scope.formatOfficesFromServer(offices);
			},
			function(error){
				Notifications.message(error);
			}
		);
    }

    $scope.loadJustifications = function() {
    	Assistance.getJustifications(
				function(justifications){
					for(var i = 0; i < justifications.length; i++){
						var id = justifications[i].id;
						$scope.model.justifications[id] = {name:justifications[i].name}
						$scope.loadJustificationStock(id);
					}
				},
				function(error){
					Notifications.message(error);
				}
			);
    }


		$scope.$on('JustificationStockChangedEvent', function(event, data) {
			if ($scope.model.session.user_id == data.user_id) {
				$scope.loadJustificationStock(data.justification_id);
			}
		});



		/*
			parsea segundos a un formato imprimible en horas.
			para las boletas de salida.
			lo saque de :
			http://stackoverflow.com/questions/6312993/javascript-seconds-to-time-string-with-format-hhmmss
		*/
		$scope.parseSecondsToDateString = function(sec) {
			var hours   = Math.floor(sec / 3600);
			var minutes = Math.floor((sec - (hours * 3600)) / 60);
			var seconds = sec - (hours * 3600) - (minutes * 60);

			if (hours   < 10) {hours   = "0"+hours;}
			if (minutes < 10) {minutes = "0"+minutes;}
			if (seconds < 10) {seconds = "0"+seconds;}
			var time    = hours+':'+minutes;
			return time;
		}




    /**
	 * Consultar datos de stock de justificacion
	 */
    $scope.loadJustificationStock = function(justificationId) {
	    Assistance.getJustificationStock($scope.model.session.user_id, justificationId,
				function(data){

						id = data.justificationId;
						stock = data.stock;

						// setep el stock en la justificacion correcta
						if(id == 'e0dfcef6-98bb-4624-ae6c-960657a9a741') {
							$scope.model.justificationAbsent = stock;
						} else if(id == '48773fd7-8502-4079-8ad5-963618abe725'){
							$scope.model.justificationCompensatory = stock;
						} else if(id == 'fa64fdbd-31b0-42ab-af83-818b3cbecf46'){
							$scope.model.justificationOut = $scope.parseSecondsToDateString(stock);
						} else if(id == '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb'){
							$scope.model.justification102 = stock;
						} else if(id == '76bc064a-e8bf-4aa3-9f51-a3c4483a729a'){
							$scope.model.justificationLao = stock;
						} else if(id == 'b70013e3-389a-46d4-8b98-8e4ab75335d0'){
							$scope.model.justificationExam = stock;
						}

				},
				function(error){
						Notifications.message(error);
				}
		);
    }


    /**
	 * cargar datos de la session
	 */
	$scope.initialize = function(){
		$scope.model.session = Session.getCurrentSession();
		if ((!$scope.model.session) || (!$scope.model.session.user_id)) {
			Notifications.message("Error: Session no definida");
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
					Notifications.message(error);
				}
			);
		}
	};

  $timeout(function() {
		$scope.initialize();
  }, 0);
});
