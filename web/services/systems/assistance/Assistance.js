var app = angular.module('mainApp');

app.service('Assistance', ['Utils','Messages','Session',

	function(Utils,Messages,Session) {

		this.getAssistanceStatusByDate = function(userId, date, callbackOk, callbackError) {
			var msg = {
				id: Utils.getId(),
				action: 'getAssistanceStatus',
				session: Session.getSessionId(),
				request:{
					user_id: userId,
					date: date
				}
			}

			Messages.send(msg,
				function(data) {
					callbackOk(data.response);
				},
				function(error) {
					callbackError(error);
				}
			);
		};


		this.getAssistanceStatus = function(userId, callbackOk, callbackError) {
			var msg = {
				id: Utils.getId(),
				action: 'getAssistanceStatus',
				session: Session.getSessionId(),
				request:{
					user_id: userId,
					date: new Date('2015-02-03T09:30:00+00:00')
				}
			}

			Messages.send(msg,
				function(data) {
					callbackOk(data.response);
				},
				function(error) {
					callbackError(error);
				}
			);
		};

		this.getAssistanceData = function(userId, callbackOk, callbackError) {
			var msg = {
				id: Utils.getId(),
				action: 'getAssistanceData',
				session: Session.getSessionId(),
				request:{
					user_id: userId
				}
			}

			Messages.send(msg,
				function(data) {
					callbackOk(data.response);
				},
				function(error) {
					callbackError(error);
				}
			);
		};


		this.getOfficesByUser = function(userId, callbackOk, callbackError) {
			var msg = {
				id: Utils.getId(),
				action: 'getOffices',
				session: Session.getSessionId(),
				request:{
					user_id: userId
				}
			}

			Messages.send(msg,
				function(data) {
					callbackOk(data.response);
				},
				function(error) {
					callbackError(error);
				}
			);
		};


		this.getJustifications = function(callbackOk, callbackError) {
			var msg = {
				id: Utils.getId(),
				action: 'getJustifications',
				session: Session.getSessionId(),
			}

			Messages.send(msg,
				function(data) {
					callbackOk(data.response.justifications);
				},
				function(error) {
					callbackError(error);
				}
			);
		};


		this.getJustificationStock = function(userId, justificationId, callbackOk, callbackError) {
			var msg = {
				id: Utils.getId(),
				action: 'getJustificationStock',
				session: Session.getSessionId(),
				request: {
					user_id: userId,
					justification_id: justificationId
				}
			}

			Messages.send(msg,
				function(data) {
					callbackOk(data.response);
				},
				function(error) {
					callbackError(error);
				}
			);
		};



		this.getJustificationRequests = function(status, group, callbackOk, callbackError){
			//TODO
			response = [
		  		{request_id:'1',user_id:"1",justification_id: "1", begin: '2015-05-13 00:00:00', end: '2015-05-13 00:00:00', state: "Desaprobada"},
	  			{request_id:'2',user_id:"1",justification_id: "2", begin: '2015-06-13 00:00:00', end: '2015-06-15 00:00:00', state: "Aprobada"}
			]

			callbackOk(response);
		}

		this.updateStatusRequestJustification = function(request_id, status, callbackOk, callbackError) {
			callbackOk(null);
		}

		this.requestLicence = function(userId, justification, callbackOk, callbackError){
			response = "ok";
			callbackOk(response);
		}

		/**
		 * Obtener solicitudes de horas extra realizadas por un determinado usuario (jefe)
		 * @param userId Id de usuario (jefe)
		 */
		this.getOvertimeRequests = function(userId, callbackOk, callbackError){
			//TODO
			var msg = {
				id: Utils.getId(),
				action: 'getOvertimeRequests',
				session: Session.getSessionId(),
				request: {
					user_id: userId //id del usuario (jefe) que solicito las horas extras
				}
			};

			response = [
		  		{id:'1', user_id:"1", begin: '2015-05-13 10:00:00', end: '2015-05-13 12:00:00', state: "PENDING", reason: "Trabajo pendiente"},
	  			{id:'2', user_id:"2", begin: '2015-06-15 12:00:00', end: '2015-06-15 15:00:00', state: "APPROVED", reason: "Adelantar trabajo"}
			];

			callbackOk(response);
		};
		
		/**
		 * Cargar nueva solicitud de horas extra
		 * @param userId (jefe) Id de usuario que solicita la hora extra
		 * @param request Solicitud de hora extra
		 */
		this.requestOvertime = function(userId, request, callbackOk, callbackError){
			var msg = {
				id: Utils.getId(),
				action: 'requestOvertime',
				session: Session.getSessionId(),
				request: {
					user_id: userId, //id del usuario al cual se solicita la hora extra
					begin: request.begin,
					end: request.end,
					reason: request.reason
				}
			};
			console.log(msg);
			callbackOk("ok");
		};
		
		
	}]
);
