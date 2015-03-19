var app = angular.module('mainApp');

app.service('Assistance',function() {

	this.getAssistanceStatus = function(userId, callbackOk, callbackError) {
		//TODO
		response = {
			status : 'Trabajando',
			start : '2015-03-13 08:25:00',
			end : '2015-03-13 14:35:00',
			logs : [
					'2015-03-13 08:00:00',
					'2015-03-13 12:00:00',
					'2015-03-13 13:30:00',
					'2015-03-13 14:45:00'
			],
			workedMinutes: '400'
		};
		callbackOk(response);
	};

	this.getAssistanceData = function(userId, callbackOk, callbackError) {
		//TODO
		response = {
			position : 'E7',
			timetable:[
				{start : '2015-03-13 09:15:00',	end : '2015-03-13 10:35:00'},
				{start : '2015-03-13 13:15:00',	end : '2015-03-13 14:35:00'}
			]
		};
		callbackOk(response);

	};

	this.getOfficesByUser = function(userId, callbackOk, callbackError) {
		//TODO
		response = [
			{id:"1",name:"Informatica"},
			{id:"2",name:"Personal"}
		];
		callbackOk(response);
	};

	this.getJustifications = function(userId, callbackOk, callbackError) {
		//TODO
		response = [
			{id:"1",name:"Ausentes con aviso"},
			{id:"2",name:"Compensatorios"},
			{id:"3",name:"Salidas Eventuales"},
			{id:"4",name:"Art. 102"},
			{id:"5",name:"Pre-examen"},
			{id:"6",name:"LAO"},

		];
		callbackOk(response);
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

	/**
	 * Obtener solicitudes de licencia del usuario
	 * Las solicitudes de licencia son aquellas peticiones de licencia futuras que aun no han sido tomadas, pueden estar aprobadas o no por el jefe o autoridad. Las fechas de inicio y/o finalizacion asociadas a las solicitudes de licencia deben ser posteriores a la fecha actual, caso contrario, la solicitud de licencia deberia ser archivada como justificacion (en el caso de que sea aprobada) o eliminada (en el caso de que este desaprobada)
	 * @param userId Id del usuario
	 * @param callbackOk Funcion a ejecutar para el caso de que los datos se reciban correctamente del servidor
	 * @param callbackError Funcion a ejecutar para el caso de que los datos se reciban erroneamente del servidor
	 */
	this.getRequestedLicences = function(userId, callbackOk, callbackError){
		//TODO
		response = [
	  		{justification_id: "1", quantity: 1, begin: '2015-05-13 00:00:00', end: '2015-05-13 00:00:00', state: "Desaprobada"},
  			{justification_id: "2", quantity: 3, begin: '2015-06-13 00:00:00', end: '2015-06-15 00:00:00', state: "Aprobada"}
		]

		callbackOk(response);
	}
});
