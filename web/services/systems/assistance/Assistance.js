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
			var sid = Session.getSessionId();
			$wamp.call('assistance.getFailsByDate', [sid, start, end])
				.then(function(res) {
					if (res != null) {
						callbackOk(res);
					} else {
						callbackError('Error');
					}
				},function(err) {
					callbackError(err);
				});
		};

		this.getFailsByFilter = function (users, offices, start, end, filter, callbackOk, callbackError) {

			var usersIds = [];
			var officesIds = [];
			var ffilter = {};

			if (users != null && users.length > 0) {
				for (var i = 0; i < users.length; i++) {
					usersIds.push(users[i].id);
				}
			}

			if (offices != null && offices.length > 0) {
				for (var i = 0; i < offices.length; i++) {
					officesIds.push(offices[i].id);
				}
			}

			// chequeo los filtros
			if (filter != null) {
				if (filter.failTypeSelected != null) {
					ffilter.failType = filter.failTypeSelected.name;
				}

				if (filter.periodicitySelected != null) {
					ffilter.periodicity = filter.periodicitySelected;
					if (filter.hoursOperator != null) {
						ffilter.hoursOperator = filter.hoursOperator.value;
						ffilter.hours = filter.hours;
						ffilter.minutes = filter.minutes;
					}
				}

				if (filter.count != null) {
					ffilter.count = filter.count;
				}
			}

			var sid = Session.getSessionId();
			$wamp.call('assistance.getFailsByFilter', [sid, usersIds, officesIds, start, end, ffilter])
				.then(function(res) {
					if (res != null) {
						callbackOk(res);
					} else {
						callbackError('Error');
					}
				},function(err) {
					callbackError(err);
				});

		}

		this.getAssistanceStatusByDate = function(userId, date, callbackOk, callbackError) {
			var sid = Session.getSessionId();
			$wamp.call('assistance.getAssistanceStatusByDate', [sid, usersId, date])
				.then(function(res) {
					if (res != null) {
						callbackOk(res);
					} else {
						callbackError('Error');
					}
				},function(err) {
					callbackError(err);
				});
		};

		this.getAssistanceStatusByUsers = function(usersIds, dates, status, callbackOk, callbackError) {
			var sid = Session.getSessionId();
			$wamp.call('assistance.getAssistanceStatusByUsers', [sid, usersIds, dates, status])
				.then(function(res) {
					if (res != null) {
						callbackOk(res);
					} else {
						callbackError('Error');
					}
				},function(err) {
					callbackError(err);
				});
		};

		this.getAssistanceData = function(userId, callbackOk, callbackError) {
			var sid = Session.getSessionId();
			$wamp.call('assistance.getAssistanceData', [sid, usersId])
				.then(function(res) {
					if (res != null) {
						callbackOk(res);
					} else {
						callbackError('Error');
					}
				},function(err) {
					callbackError(err);
				});
		};


		this.getSchedules = function(userId, date, callbackOk, callbackError) {
			var sid = Session.getSessionId();
			$wamp.call('assistance.getSchedules', [sid, usersId, date])
				.then(function(res) {
					if (res != null) {
						callbackOk(res);
					} else {
						callbackError('Error');
					}
				},function(err) {
					callbackError(err);
				});
		};


		/*
		schedule:{
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

		this.persistSchedule = function(schedule, callbackOk, callbackError) {
			var sid = Session.getSessionId();
			$wamp.call('assistance.persistSchedule', [sid, schedule])
				.then(function(res) {
					if (res != null) {
						callbackOk(res);
					} else {
						callbackError('Error');
					}
				},function(err) {
					callbackError(err);
				});
		};


    this.deleteSchedule = function(id, callbackOk, callbackError) {
			var sid = Session.getSessionId();
			$wamp.call('assistance.deleteSchedule', [sid, id])
				.then(function(res) {
					if (res != null) {
						callbackOk(res);
					} else {
						callbackError('Error');
					}
				},function(err) {
					callbackError(err);
				});
    };




		this.getJustifications = function(callbackOk, callbackError) {
			var sid = Session.getSessionId();
			$wamp.call('assistance.justifications.getJustifications', [sid])
				.then(function(res) {
					if (res != null) {
						callbackOk(res);
					} else {
						callbackError('Error');
					}
				},function(err) {
					callbackError(err);
				});
		};

		this.getJustificationsByUser = function(userId, callbackOk, callbackError) {
			var sid = Session.getSessionId();
			$wamp.call('assistance.justifications.getJustificationsByUser', [sid, userId])
				.then(function(res) {
					if (res != null) {
						callbackOk(res);
					} else {
						callbackError('Error');
					}
				},function(err) {
					callbackError(err);
				});
		};


		this.getJustificationStock = function(userId, justificationId, date, period, callbackOk, callbackError) {
			var sid = Session.getSessionId();
			$wamp.call('assistance.justifications.getJustificationsStock', [sid, userId, justificationId, date, period])
				.then(function(res) {
					if (res != null) {
						callbackOk(res);
					} else {
						callbackError('Error');
					}
				},function(err) {
					callbackError(err);
				});
		};

    /**
     * Actualizar stock de la justificacion de un usuario
     * @param {userId} userId
     * @param {justificationId} justificationId
     * @param {stock} stock
     */
    this.updateJustificationStock = function(userId, justificationId, stock, callbackOk, callbackError) {
			var sid = Session.getSessionId();
			$wamp.call('assistance.justifications.updateJustificationStock', [sid, userId, justificationId, stock])
				.then(function(res) {
					if (res != null) {
						callbackOk(res);
					} else {
						callbackError('Error');
					}
				},function(err) {
					callbackError(err);
				});
		};

		this.getJustificationRequestsByDate = function(status, usersIds, start, end, callbackOk, callbackError){
			var sid = Session.getSessionId();
			$wamp.call('assistance.justifications.getJustificationsRequestsByDate', [sid, userIds, start, end, status])
				.then(function(res) {
					if (res != null) {
						callbackOk(res);
					} else {
						callbackError('Error');
					}
				},function(err) {
					callbackError(err);
				});
		}

		this.getJustificationRequestsToManage = function(status, group, callbackOk, callbackError){
			var sid = Session.getSessionId();
			$wamp.call('assistance.justifications.getJustificationsRequestsToManage', [sid, status, group])
				.then(function(res) {
					if (res != null) {
						callbackOk(res);
					} else {
						callbackError('Error');
					}
				},function(err) {
					callbackError(err);
				});
		}


		this.getJustificationRequests = function(status, callbackOk, callbackError){
			var sid = Session.getSessionId();
			$wamp.call('assistance.justifications.getJustificationsRequests', [sid, status])
				.then(function(res) {
					if (res != null) {
						callbackOk(res);
					} else {
						callbackError('Error');
					}
				},function(err) {
					callbackError(err);
				});
		}


		this.updateJustificationRequestStatus = function(requestId, status, callbackOk, callbackError) {
			var sid = Session.getSessionId();
			$wamp.call('assistance.justifications.updateJustificationRequestStatus', [sid, requestId, status])
				.then(function(res) {
					if (res != null) {
						callbackOk(res);
					} else {
						callbackError('Error');
					}
				},function(err) {
					callbackError(err);
				});
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
