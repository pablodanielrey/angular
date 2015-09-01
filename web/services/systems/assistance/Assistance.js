var app = angular.module('mainApp');

app.service('Assistance', ['Utils','Session','Office',

	function(Utils, Session, Office) {

		this.getOfficesUsers = function(offices, cok, cerr) {
			var sid = Session.getSessionId();
			Office.getOfficesUsers(offices, cok, cerr);
		}

		this.getUsersInOfficesByRole = function(role, cok, cerr) {
			Office.getUserInOfficesByRole(role,cok,cerr);
		}

		this.getOfficesByUserRole = function(userId, role, tree, cok, cerr) {
			Office.getOfficesByUserRole(userId, role, tree, cok, cerr);
		}

		this.getOfficesByUser = function(userId, callbackOk, callbackError) {
			var msg = {
				id: Utils.getId(),
				action: 'getOffices',
				session: Session.getSessionId(),
				request:{
					user_id: userId
				}
			}

		};

		this.getUserOfficeRoles = function(callbackOk, callbackError) {
			var msg = {
				id: Utils.getId(),
				action: 'getUserOfficeRoles',
				session: Session.getSessionId(),
				request:{
				}
			}

		};


		this.getFailsByDate = function(start, end, callbackOk, callbackError) {
				var msg = {
					id: Utils.getId(),
					action: 'getFailsByDate',
					session: Session.getSessionId(),
					request: {
						start: start,
						end: end
					}
				}

		};

		this.getFailsByFilter = function (users, offices, start, end, filter, callbackOk, callbackError) {
			var msg = {
				id: Utils.getId(),
				action: 'getFailsByFilter',
				session: Session.getSessionId(),
				request: {
					start: start,
					end: end
				}
			}

			if (users != null && users.length > 0) {
				var usersIds = [];
				for (var i = 0; i < users.length; i++) {
					usersIds.push(users[i].id);
				}
				msg.request.users = usersIds;
			}

			if (offices != null && offices.length > 0) {
				var officesIds = [];
				for (var i = 0; i < offices.length; i++) {
					officesIds.push(offices[i].id);
				}
				msg.request.offices = officesIds;
			}

			// chequeo los filtros
			if (filter != null) {
				msg.request.filter = {};

				if (filter.failTypeSelected != null) {
					msg.request.filter.failType = filter.failTypeSelected.name;
				}

				if (filter.periodicitySelected != null) {
					msg.request.filter.periodicity = filter.periodicitySelected;
					if (filter.hoursOperator != null) {
						msg.request.filter.hoursOperator = filter.hoursOperator.value;
						msg.request.filter.hours = filter.hours;
						msg.request.filter.minutes = filter.minutes;
					}
				}

				if (filter.count != null) {
					msg.request.filter.count = filter.count;
				}
			}

		}

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

		};

		this.getAssistanceStatusByUsers = function(usersIds, dates, status, callbackOk, callbackError) {
			var msg = {
				id: Utils.getId(),
				action: 'getAssistanceStatusByUsers',
				session: Session.getSessionId(),
				request:{
					usersIds: usersIds,
					dates: dates,
					status: status
				}
			}

		};

		this.getAssistanceStatus = function(userId, callbackOk, callbackError) {
			var msg = {
				id: Utils.getId(),
				action: 'getAssistanceStatus',
				session: Session.getSessionId(),
				request:{
					user_id: userId,
					date: new Date()
				}
			}

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

		};


		this.getSchedules = function(userId,date, callbackOk, callbackError) {
			var msg = {
				id: Utils.getId(),
				action: 'getSchedules',
				session: Session.getSessionId(),
				request:{
					user_id: userId,
				}
			}

			if (date != null) {
				msg.request.date = date;
			}

		};


		/*
		request:{
			user_id:"id del Usuario",
			date:"fecha de que se empieza a utilizar el schedule, si no se envia se toma la fecha actual",
			start:"hora de inicio del turno",
			end:"hora de fin de turno",
			daysOfWeek:[],
			isDayOfWeek:"es dia de la semana, si no se envia se toma como false",
			isDayOfMonth:"es dia un dia del mes, si no se envia se toma como false",
			isDayOfYear:"es dia del año, si no se envia se toma como false"
		}
		*/

		this.newSchedule = function(request, callbackOk, callbackError) {
			var msg = {
				id: Utils.getId(),
				action: 'newSchedule',
				session: Session.getSessionId(),
				request:request
			}

		};


    this.deleteSchedule = function(scheduleId, callbackOk, callbackError) {
      var msg = {
				id: Utils.getId(),
				action: 'deleteSchedule',
				session: Session.getSessionId(),
        request: {
					schedule_id: scheduleId
				}
			};

    };




		this.getJustifications = function(callbackOk, callbackError) {
			var msg = {
				id: Utils.getId(),
				action: 'getJustifications',
				session: Session.getSessionId(),
			};

		};

		this.getJustificationsByUser = function(userId, callbackOk, callbackError) {
			var msg = {
				id: Utils.getId(),
				action: 'getJustificationsByUser',
				session: Session.getSessionId(),
				request:{
					userId: userId
				}
			}
		};


		this.getJustificationStock = function(userId, justificationId, date, period, callbackOk, callbackError) {
			var msg = {
				id: Utils.getId(),
				action: 'getJustificationStock',
				session: Session.getSessionId(),
				request: {
					user_id: userId,
					justification_id: justificationId
				}
			};

			if (date != null) {
				msg.request.date = date;
			}

			if (period != null) {
				msg.request.period = period;
			}
		};

    /**
     * Actualizar stock de la justificacion de un usuario
     * @param {userId} userId
     * @param {justificationId} justificationId
     * @param {stock} stock
     */
    this.updateJustificationStock = function(userId, justificationId, stock,callbackOk,callbackError) {
			var msg = {
				id: Utils.getId(),
				action: 'updateJustificationStock',
				session: Session.getSessionId(),
				request: {
					userId: userId,
 					justificationId: justificationId,
					stock: stock
				}
			};
		};

		this.getJustificationRequestsByDate = function(status, usersIds, start, end, callbackOk, callbackError){
			var msg = {
				id: Utils.getId(),
				action: 'getJustificationRequestsByDate',
				session: Session.getSessionId(),
				request: {
				}
			}

			if (status != null) {
				msg.request.status = status;
			}

			if (usersIds != null) {
				msg.request.usersIds = usersIds;
			}

			if (start != null) {
				msg.request.start = start;
			}

			if (end != null) {
				msg.request.end = end;
			}
		}

		this.getJustificationRequestsToManage = function(status, group, callbackOk, callbackError){
			var msg = {
				id: Utils.getId(),
				action: 'getJustificationRequestsToManage',
				session: Session.getSessionId(),
				request: {
				}
			}

			if (status != null) {
				msg.request.status = status;
			}

			if (group != null) {
				msg.request.group = group;
			}
		}


		this.getJustificationRequests = function(status, callbackOk, callbackError){
			var msg = {
				id: Utils.getId(),
				action: 'getJustificationRequests',
				session: Session.getSessionId(),
				request: {
				}
			}

			if (status != null) {
				msg.request.status = status;
			}
		}


		this.updateJustificationRequestStatus = function(requestId, status, callbackOk, callbackError) {
			var msg = {
				id: Utils.getId(),
				action: 'updateJustificationRequestStatus',
				session: Session.getSessionId(),
				request: {
					request_id: requestId,
					status: status
				}
			}
		};

		this.requestJustification = function(userId, justification, status, callbackOk, callbackError) {
			var msg = {
				id: Utils.getId(),
				action: 'requestJustification',
				session: Session.getSessionId(),
				request: {
					user_id: userId,
					justification_id: justification.id,
					begin: justification.begin
				}
			}

			if (!(typeof justification.end === 'undefined')) {
				msg.request.end = justification.end;
			}

			if (!(typeof status === 'undefined')) {
				msg.request.status = status;
			}
		}

		this.requestJustificationRange = function(userId, justification, status, callbackOk, callbackError) {
			var msg = {
				id: Utils.getId(),
				action: 'requestJustificationRange',
				session: Session.getSessionId(),
				request: {
					user_id: userId,
					justification_id: justification.id,
					begin: justification.begin,
					end: justification.end
				}
			}

			if (!(typeof status === 'undefined')) {
				msg.request.status = status;
			}
		}



		/**
		 * Obtener solicitudes de horas extra realizadas por el usuario que esta logueado
		 */
		this.getOvertimeRequests = function(status, callbackOk, callbackError){
			var msg = {
				id: Utils.getId(),
				action: 'getOvertimeRequests',
				session: Session.getSessionId(),
				request: {
				}
			};

			if (status != null) {
				msg.request.status = status;
			}
		};


		/**
		* Obtener solicitudes de horas extra realizadas por el usuario que esta logueado
		*/
		this.getOvertimeRequestsToManage = function(status, group, callbackOk, callbackError){
			var msg = {
				id: Utils.getId(),
				action: 'getOvertimeRequestsToManage',
				session: Session.getSessionId(),
				request: {
				}
			};

			if (status != null) {
				msg.request.status = status;
			}

			if (group != null) {
				msg.request.group = group;
			}
		};


		/**
		 * Cargar nueva solicitud de horas extra
		 * @param userId id del usuario al cual se solicita la hora extra
		 * @param request Solicitud de hora extra
		 */
		this.requestOvertime = function(userId, request, callbackOk, callbackError){
			var msg = {
				id: Utils.getId(),
				action: 'requestOvertime',
				session: Session.getSessionId(),
				request: {
					user_id: userId, 						//id del usuario al cual se solicita la hora extra
					begin: request.begin,
					end: request.end,
					reason: request.reason
				}
			};
		};

		/**
		 * Actualizar estado de solicitud de hora extra
		 * @param requestId Id de la solicitud
		 * @param state Nuevo estado de la solicitud
		 */
		this.updateRequestOvertimeStatus = function(requestId, state, callbackOk, callbackError) {
			var msg = {
				id: Utils.getId(),
				action: 'updateOvertimeRequestStatus',
				session: Session.getSessionId(),
				request: {
					request_id: requestId,
					status: state
				}
			};
		}


		/**
		*	Obtiene las justificaciones especiales que puede solicitar
		*/
		this.getSpecialJustifications = function(callbackOk, callbackError) {
			var msg = {
				id: Utils.getId(),
				action: 'getSpecialJustifications',
				session: Session.getSessionId(),
				request: {
				}
			};
		};



    /**
     * solicitar justificacion general
     * @param {type} justification Datos de la justificacion
     * @param {type} callbackOk
     * @param {type} callbackError
     * @returns {undefined}
     */
    this.requestGeneralJustification = function(justification, callbackOk, callbackError) {
			var msg = {
				id: Utils.getId(),
				action: 'requestGeneralJustification',
				session: Session.getSessionId(),
				request: {
					justification_id: justification.id,
					begin: justification.begin
				}
			};

			if (!(typeof justification.end === 'undefined')) {
				msg.request.end = justification.end;
			}
		};


		/**
     * solicitar justificacion general en un rango
     * @param {type} justification Datos de la justificacion
     * @param {type} callbackOk
     * @param {type} callbackError
     * @returns {undefined}
     */
    this.requestGeneralJustificationRange = function(justification, callbackOk, callbackError) {
			var msg = {
				id: Utils.getId(),
				action: 'requestGeneralJustificationRange',
				session: Session.getSessionId(),
				request: {
					justification_id: justification.id,
					begin: justification.begin,
					end: justification.end
				}
			};
		};


    /**
     * solicitar justificaciones generales
     * @param {type} callbackOk
     * @param {type} callbackError
     * @returns {undefined}
     */
    this.getGeneralJustificationRequests = function(callbackOk, callbackError){
      var msg = {
				id: Utils.getId(),
				action: 'getGeneralJustificationRequests',
				session: Session.getSessionId()
			};
    };

    this.deleteGeneralJustificationRequest = function(requestId, callbackOk, callbackError){
      var msg = {
				id: Utils.getId(),
				action: 'deleteGeneralJustificationRequest',
				session: Session.getSessionId(),
        request: {
					request_id: requestId
				}
			};
    };



  this.getPosition = function(userId, callbackOk, callbackError){
    var msg = {
				id: Utils.getId(),
				action: 'getPosition',
				session: Session.getSessionId(),
        request: {
					userId: userId
				}
			};
  };

  /**
   * Actualizar cargo del usuario
   * @param {userId} userId
   * @param {justificationId} justificationId
   * @param {stock} stock
   */
  this.updatePosition = function(userId, position, callbackOk,callbackError) {
    var msg = {
      id: Utils.getId(),
      action: 'updatePosition',
      session: Session.getSessionId(),
      request: {
        userId: userId,
        position: position
      }
    };
  }


}]);
