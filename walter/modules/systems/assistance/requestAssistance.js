var app = angular.module('mainApp');

app.controller('RequestAssistanceCtrl', function($scope, $rootScope, $timeout) {
	
	$scope.model = {
		justifications : [], //auxiliar para almacenar las justificaciones del usuario y su stock asociado
		requestLicences : [], //auxiliar para almacenar los datos de las solicitudes de licencias futuras
	};
	

	/*
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
	 *
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
	
	$scope.loadRequestLicences = function() {
		Assistance.getRequestLicences($scope.model.session.user_id,
			function(requestLicences){
				for(i in requestLicences){
					
				}
			},
			function(error){
				alert(error);
			}
		);
	}*/

    $timeout(function() {
        
    }, 0);

});
