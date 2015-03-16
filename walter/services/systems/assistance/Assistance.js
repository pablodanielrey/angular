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
});
