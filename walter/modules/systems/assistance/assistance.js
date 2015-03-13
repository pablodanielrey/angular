var app = angular.module('mainApp');

app.controller('AssistanceCtrl', function($scope, $timeout, $window, Profiles, Session, Users, Assistance) {

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
			timetable:[], //fracciones horarias del dia actual
    	},
    	offices : [] //oficinas del usuario
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
		for (office in officesFromServer){
			$scope.model.offices.push(officesFromServer[office].name);
		}
	};

	/**
	 * Dar formato a los datos del estado de asistencia recibidos del servidor
	 */
	$scope.formatAssistanceStatusFromServer = function(assistanceStatusFromServer){
		$scope.model.assistanceStatus.status = assistanceStatusFromServer.status;
		
		var start = new Date(assistanceStatusFromServer.start);
		$scope.model.assistanceStatus.start = start.getHours() + ":" + start.getMinutes();
		
		var end = new Date(assistanceStatusFromServer.end);
		$scope.model.assistanceStatus.end = end.getHours() + ":" + end.getMinutes();
		
		var workedMinutes = assistanceStatusFromServer.workedMinutes;
		var workedH = Math.floor(workedMinutes/60);
		var workedM = workedMinutes % 60;
		$scope.model.assistanceStatus.workedTime = workedH + ":" + workedM;
	
	};

	/**
	 * Dar formato a los datos de asistencia recibidos del servidor
	 */
	$scope.formatAssistanceDataFromServer = function(assistanceDataFromServer){
		$scope.model.assistanceData.position = assistanceDataFromServer.position;

		for(var time in assistanceDataFromServer.timetable){
			var start = new Date(assistanceDataFromServer.timetable[time].start);
			var startHour = start.getHours() + ":" + start.getMinutes();
		
			var end = new Date(assistanceDataFromServer.timetable[time].end);
			var endHour = end.getHours() + ":" + end.getMinutes()
			
			$scope.model.assistanceData.timetable.push(startHour + " / " + endHour);
			

		}
	};

	/**
	 * consultar datos de asistencia
	 */
	$scope.loadAssistanceStatus = function(){
		Assistance.getAssistanceStatus($scope.model.session.user_id, 
			function(assistanceStatus){
				$scope.formatAssistanceStatusFromServer(assistanceStatus);
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
