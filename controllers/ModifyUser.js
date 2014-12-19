
app.controller("ModifyUserController", ["$scope", "$cookies", "WebSocket", "Session", "uuid4", function($scope, $cookies, WebSocket, Session, uuid4){

	var ids = new Array(); //identificador de peticiones enviadas al server
	
	
	//***** CONSULTAR DATOS DE SESSION *****
	var id =  uuid4.generate();
	ids[id] = "userSessionData";
		
	//Al acceder al controlador se deben obtener los datos de usuario del servidor
	var data = {
		"id" : id,
		"action" : "createAccountRequest", //TODO MODIFICAR Y ASIGNAR EL CONTROLADOR CUANDO ESTE HECHO userSessionData
		"session" : Session.getSessionId(),
	}
		
	WebSocket.send(JSON.stringify(data));
	
	
	
	/**
	 * Analizar evento onMessage para determinar si es una respuesta a la peticion de los datos de usuario del servidor
	 */
	$scope.$on('onMessage', function(event, data){
		alert(data);
		var response = JSON.parse(data);
				
		if(response.id == undefined)
			return;
		
		if(ids[response.id] == undefined)
			return;
		
		action = ids[response.id];
		delete ids[response.id]
		 
		if(response.error != undefined){
			var data = {
				"message" : response.error,
			}
			$rootScope.$broadcast("onAppError", JSON.stringify(data));
		}

		if(response.ok != undefined){
			if(action = "userSessionData"){
				$scope.name =  response.name
				$scope.lastname =  response.lastname
				$scope.dni =  response.dni
				$scope.mail =  response.mail
				$scope.telephone = response.telephone
				$scope.adress = response.adress
				$scope.bornCity = response.bornCity
				$scope.country = response.country
				$scope.genre = response.genre
				$scope.studentNumber = response.studentNumber
				$scope.personalEmail = response.personaEmail
				$scope.email = response.email
				return;
			} /*else if(action = "modifyUserSessionData") {
				var data = {
					"message" : "Modificacion realizada exitosamente",
				}
				$rootScope.$broadcast("onAppMessage", JSON.stringify(data));
				return;
			}*/
		}
	});


	/**
	 * Modificar datos de usuario de la session
	 *
	$scope.modify = function(){
		var data = {
			"session" : $cookies.fceSession,
			"name" : $scope.name,
			"lastname" : $scope.lastname,
			"dni" : $scope.dni,
			"mail" : $scope.mail,
			"action" : "modifyUserSessionData",
		}
		
		WebSocket.send(JSON.stringify(data));
	}*/
	
}]); 
