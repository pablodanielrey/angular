var app = angular.module('mainApp');

app.service('Assistance', ['Utils','Messages','Session',

	function(Utils,Messages,Session) {

		/*
		Obtiene todos los usuarios de las oficinas pasadas como parametro
		*/

		this.getOfficesUsers = function(offices, callbackOk, callbackError) {
			var msg = {
				id: Utils.getId(),
				action: 'getOfficesUsers',
				session: Session.getSessionId(),
				request: {
					offices: offices
				}
			}

			Messages.send(msg,
				function(data) {
					if (typeof data.error === 'undefined') {
						callbackOk(data.response.users);
					} else {
						callbackError(data.error);
					}
				});
		}

		/*
			Obtiene los usuarios que se encuentran dentro de las oficinas a las cuales el usuario loggeado tiene
			un rol determinado.
		*/
		this.getUsersInOfficesByRole = function(role, callbackOk, callbackError) {
			var msg = {
				id: Utils.getId(),
				action: 'getUserInOfficesByRole',
				session: Session.getSessionId(),
				request: {
					tree: true
				}
			}

			if (role != null) {
				msg.request.role = role;
			}

			Messages.send(msg,
				function(data) {
					if (typeof data.error === 'undefined') {
						callbackOk(data.response.users);
					} else {
						callbackError(data.error);
					}
				});
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

				Messages.send(msg,
					function(data) {
						if (typeof data.error === 'undefined') {
							callbackOk(data.response);
						} else {
							callbackError(data.error);
						}
					});
		};

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
					if (typeof data.error === 'undefined') {
						callbackOk(data.response);
					} else {
						callbackError(data.error);
					}
				});
		};

		this.getAssistanceStatusByUsers = function(usersIds, dates, callbackOk, callbackError) {
			var msg = {
				id: Utils.getId(),
				action: 'getAssistanceStatusByUsers',
				session: Session.getSessionId(),
				request:{
					usersIds: usersIds,
					dates: dates
				}
			}

			Messages.send(msg,
				function(data) {
					if (typeof data.error === 'undefined') {
						callbackOk(data.response);
					} else {
						callbackError(data.error);
					}
				});
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

			Messages.send(msg,
				function(data) {
					if (typeof data.error === 'undefined') {
						callbackOk(data.response);
					} else {
						callbackError(data.error);
					}
				});
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
					if (typeof data.error === 'undefined') {
						callbackOk(data.response);
					} else {
						callbackError(data.error);
					}
				});
		};


		this.getOfficesByUserRole = function(userId,role,tree, callbackOk, callbackError) {
			var msg = {
				id: Utils.getId(),
				action: 'getOfficesByUserRole',
				session: Session.getSessionId(),

				request:{
					user_id: userId,
					tree:tree
				}
			}

			if (role != null) {
				msg.request.role = role;
			}

			Messages.send(msg,
				function(data) {
					if (typeof data.error === 'undefined') {
						callbackOk(data.response.offices);
					} else {
						callbackError(data.error);
					}
				});
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
					if (typeof data.error === 'undefined') {
						callbackOk(data.response);
					} else {
						callbackError(data.error);
					}
				});
		};

		this.getUserOfficeRoles = function(callbackOk, callbackError) {
			var msg = {
				id: Utils.getId(),
				action: 'getUserOfficeRoles',
				session: Session.getSessionId(),
				request:{
				}
			}

			Messages.send(msg,
				function(data) {
					if (typeof data.error === 'undefined') {
						callbackOk(data.response.roles);
					} else {
						callbackError(data.error);
					}
				});
		};


		this.getJustifications = function(callbackOk, callbackError) {
			var msg = {
				id: Utils.getId(),
				action: 'getJustifications',
				session: Session.getSessionId(),
			}

			Messages.send(msg,
				function(data) {
					if (typeof data.error === 'undefined') {
						callbackOk(data.response.justifications);
					} else {
						callbackError(data.error);
					}
				});
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

			Messages.send(msg,
				function(data) {
					if (typeof data.error === 'undefined') {
						callbackOk(data.response);
					} else {
						callbackError(data.error);
					}
				});
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

			Messages.send(msg,
				function(data) {
					if (typeof data.error === 'undefined') {
						callbackOk(data.response.requests);
					} else {
						callbackError(data.error);
					}
			});
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

			Messages.send(msg,
				function(data) {
					if (typeof data.error === 'undefined') {
						callbackOk(data.response.requests);
					} else {
						callbackError(data.error);
					}
			});
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

			Messages.send(msg,
				function(data) {
					if (typeof data.error === 'undefined') {
						callbackOk(data.response.requests);
					} else {
						callbackError(data.error);
					}
				});
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

			Messages.send(msg,
				function(data) {
					if (typeof data.error === 'undefined') {
						callbackOk(data.ok);
					} else {
						callbackError(data.error);
					}
				}
			);

		}

		this.requestJustification = function(userId, justification, callbackOk, callbackError) {
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

			Messages.send(msg,
				function(data) {
					if (typeof data.error === 'undefined') {
						callbackOk(data.response);
					} else {
						callbackError(data.error);
					}
				});
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

			Messages.send(msg,
				function(data) {
					if (typeof data.error === 'undefined') {
						callbackOk(data.response.requests);
					} else {
						callbackError(data.error);
					}
				});
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

			Messages.send(msg,
				function(data) {
					if (typeof data.error === 'undefined') {
						callbackOk(data.response.requests);
					} else {
						callbackError(data.error);
					}
				});
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
			Messages.send(msg,
				function(data) {
					if (typeof data.error === 'undefined') {
						callbackOk(data.ok);
					} else {
						callbackError(data.error);
					}
				});
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
			Messages.send(msg,
				function(data) {
					if (typeof data.error === 'undefined') {
						callbackOk(data.ok);
					} else {
						callbackError(data.error);
					}
				});
		}



	}]
);
