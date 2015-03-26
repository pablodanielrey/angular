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
					callbackOk(data.response);
				},
				function(error) {
					callbackError(error);
				}
			);
		};


		this.getJustificationStock = function(userId, justificationId, callbackOk, callbackError) {
			//TODO
			switch(justificationId){
				case "1":
					response = 2;
				break;
				case "2":
					response = 4;
				break;
				case "3":
					response = 1;
				break;
				case "4":
					response = 3;
				break;
				case "5":
					response = 3;
				break;
				case "6":
					response = 20;
				break;
			}

			callbackOk(response);
		};


		//stock del mes que es generalmente el que le interesa visualizar al usuario
		this.getJustificationActualStock = function(userId, justificationId, callbackOk, callbackError) {
			//TODO
			switch(justificationId){
				case "1":
					response = 1;
				break;
				case "2":
					response = 2;
				break;
				case "3":
					response = 0;
				break;
				case "4":
					response = 2;
				break;
				case "5":
					response = 2;
				break;
				case "6":
					response = 10;
				break;
			}

			callbackOk(response);
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
	}]
);
